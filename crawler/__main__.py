"""
Threaded crawler based on Mercator scheme, specialized for Twitter.
"""

from threading import Thread, Event, Timer as TimerTrigger, Condition
from queue import Queue, Empty
from typing import Any, Callable
import requests
from bs4 import BeautifulSoup
import time
from math import ceil
from icecream import ic
from urllib.parse import urlparse, urljoin
import random
from threading import current_thread
from unidecode import unidecode
import argparse
import os.path as osp, os
import http.client as hc
import re
import json
import csv

jsonDecoder = json.JSONDecoder()

def thread_id():
    return current_thread().getName()


class Timer:
    """This context manager allows timing blocks of code."""
    def __init__(self):
        self._timer = None
        self._elapsed = None
    
    def __enter__(self) -> None:
        self._timer = time.time()
        return self

    def __exit__(self, *_: list) -> None:
        self._elapsed = time.time() - self._timer

    def __float__(self):
        return self._elapsed or time.time() - self._timer


class Spider:
    def __init__(self):
        # timing/ sync
        self.interrupt = Event()
        self.frontier_cv = Condition()

        # collection
        self.collected: set[str] = set()
        self.front_queues: list[Queue[str]] = []  # a front queue for each priority level
        self.back_queues: dict[str, Queue[str]] = {}  # will have back queue for each domain
        self.ready_queue: Queue[str] = Queue()  # lowest = highest priority, iterates thru item to handle ties
        self.domain_profiles: dict[str: dict[str, Any]] = {}

        # state
        self.num_threads = None
        self.is_crawling = False

    def crawl(
            self,
            seeds: set[str],
            on_content: Callable[[str, str], None],
            url_priority: Callable[[str], int] = lambda _: 0,
            k_weights: tuple[float] = (1,),
            timeout: float = None,
        ) -> None:
        self._initialize_crawl(seeds, k_weights, url_priority)
        workers = [self._make_worker(on_content, url_priority, k_weights) for _ in range(self.num_threads)]
        self.is_crawling = True
        for t in workers: t.start()
        try: self.interrupt.wait(timeout = timeout)
        except KeyboardInterrupt: pass
        self.signal_stop_crawl()
        for t in workers: t.join()
        self._reset()

    
    def should_crawl(self) -> bool:
        return not self.interrupt.is_set()


    def signal_stop_crawl(self) -> None:
        self.interrupt.set()


    def _crawl_worker(
            self,
            on_content: Callable[[str, str], None],
            url_priority: Callable[[str], int],
            k_weights: tuple[int]
        ) -> None:
        urls_crawled = 0  # number of urls crawled
        errs = 0  # number of errors during scraping
        latency_sum = 0
        ic(f'starting thread {thread_id()}')

        with Timer() as t:
            while self.should_crawl():
                try: ready_time, target_domain = self.ready_queue.get(timeout=3)
                except Empty: continue
                latency = time.time() - ready_time
                latency_sum += latency
                target_queue = self.back_queues[target_domain]
                try: target_url = target_queue.get(timeout=3)
                except Empty: continue
                try:
                    conn = hc.HTTPSConnection(target_domain.split("://")[1][:-1])
                    conn.set_debuglevel(0) #TODO get rid
                    conn.request("GET", target_url)
                    resp = conn.getresponse()
                    fetched_at = time.time()
                    if resp.status != 200: raise ConnectionError('received non-200 code')
                    content, urls = Spider._parse_html(resp.read(), target_domain)
                    self._queue_new_urls(urls, url_priority)
                    if content: on_content(target_url, content, latency)
                except (requests.exceptions.ConnectionError, ConnectionError):
                    fetched_at = time.time()
                    errs += 1
                urls_crawled += 1
                
                if target_queue.empty(): self._recycle_back_queue(target_domain, target_queue, fetched_at, k_weights)
                else: self._queue_domain(fetched_at, target_domain)
                   
        ic(thread_id(), errs, urls_crawled, latency_sum, float(t))


    def _initialize_crawl(self, seeds: set[str], k_weights: tuple[int], url_priority: Callable[[str], int]) -> None:
        self.front_queues = [Queue() for _ in range(len(k_weights))]
        for seed in seeds:
            self._mark_collected(seed)
            domain = Spider.get_domain(seed)
            self._add_to_frontier(seed, url_priority(seed))
            if domain not in self.back_queues: self._initialize_new_domain(domain, Queue())
            self.back_queues[domain].put(seed)
        self.num_threads = min(ceil(len(self.back_queues) / 2), 64)  # per mercator reccomendations


    def _add_to_frontier(self, url: str, priority: int) -> None:
        with self.frontier_cv:
            self.front_queues[priority].put(url)
            self.frontier_cv.notify_all()


    def _pull_from_frontier(self, k_weights: tuple[int]) -> str:
        with self.frontier_cv:
            while not (available := [i for i, queue in enumerate(self.front_queues) if not queue.empty()]):
                self.frontier_cv.wait()
            weights = [k_weights[i] for i in available]
            return self.front_queues[random.choices(available, weights=weights, k=1).pop()].get()

    @staticmethod
    def robot_valid_href(href: str) -> bool:
        if not href:
            return False
        # Note still must abide by crawl-delay = 1
        # TODO make RE patterns const expr
        valid = True
        valid &= (not not re.compile("twitter.com").search(href)) or href[0] == "/"
        valid &= not re.compile("/search/realtime").search(href)
        valid &= not re.compile("/search/users").search(href)
        valid &= not re.compile(r"/search/.+/grid").search(href)

        valid &= not re.compile(r"/.+/followers").search(href)
        valid &= not re.compile(r"/.+/following").search(href)

        valid &= not re.compile("/oauth").search(href)
        valid &= not re.compile("/1/oauth").search(href)

        valid &= not re.compile("/i/streams").search(href)
        valid &= not re.compile("/i/hello").search(href)
        
        valid &= not re.compile("/account/deactivated").search(href)
        valid &= not re.compile("/settings/deactivated").search(href)
        return valid


    def _profile_domain(self, url: str) -> dict:
        return {
            'crawl_delay': 1,
        }

    def _make_worker(self, *args, **kwargs):
        return Thread(target = self._crawl_worker, args = args, kwargs = kwargs, daemon = True)


    def _queue_new_urls(self, urls, url_priority):
        for new_url in urls - self.collected:
            self._mark_collected(new_url)
            if Spider.get_domain(new_url) in self.back_queues:
                self._add_to_frontier(new_url, url_priority(new_url))

    def _queue_domain(self, fetched_at, domain):
        ready_at = fetched_at + self.domain_profiles[domain]['crawl_delay']
        wait_time = ready_at - time.time()
        if wait_time > 0: TimerTrigger(wait_time, lambda: self.ready_queue.put((ready_at, domain))).start()
        else: self.ready_queue.put((ready_at, domain))


    def _initialize_new_domain(self, new_domain, target_queue):
        self.domain_profiles[new_domain] = self._profile_domain(new_domain)
        self.back_queues[new_domain] = target_queue
        self.ready_queue.put((time.time(), new_domain))


    def _recycle_back_queue(
            self,
            target_domain: str,
            target_queue: Queue[str],
            fetched_at: float,
            k_weights: tuple[int]
        ) -> None:
        del self.back_queues[target_domain]
        while self.should_crawl():
            new_url = self._pull_from_frontier(k_weights)
            new_domain = Spider.get_domain(new_url)
            if new_domain in self.back_queues:  # currently active
                self.back_queues[new_domain].put(new_url)
            elif new_domain in self.domain_profiles:  # seen before but not active
                target_queue.put(new_url)
                self.back_queues[new_domain] = target_queue
                self._queue_domain(fetched_at, new_domain)
                break
            else:  # never seen before
                target_queue.put(new_url)
                self._initialize_new_domain(new_domain, target_queue)
                break

    @staticmethod
    def tweetFilter(tag):
        return tag.has_attr("data-item-type") and tag["data-item-type"] == "tweet"

    @staticmethod
    def scrapeTweet(soup):
        tweets = []
        for tag in soup.find_all(Spider.tweetFilter):
            # Get immediate subclass with tweet data
            dataTag = tag.find("div")
            if (not dataTag.has_attr("data-reply-to-users-json")):
                continue
            tweetTag = dataTag.find("p", class_=re.compile("tweet-text"))
            
            userJsonData = jsonDecoder.decode(dataTag["data-reply-to-users-json"])
            
            permaPath = dataTag["data-permalink-path"]
            tweetText = tweetTag.get_text() #TODO: Make unicode fun
            primaryUser = userJsonData[0]
            tweets.append((primaryUser["id_str"], primaryUser["screen_name"], primaryUser["name"], permaPath, tweetText))
        return tweets
        
    @staticmethod
    def _parse_html(text: str, target_domain: str) -> tuple[tuple[Any], set[str]]:
        soup = BeautifulSoup(text, 'html.parser')
        urls = {urljoin(target_domain, url['href']) for url in soup.find_all(href=Spider.robot_valid_href)}
        content = Spider.scrapeTweet(soup)
        return content, urls

    def _mark_collected(self, url: str) -> None:
        self.collected.add(url if not url.endswith('/') else url[:-1])

    def _reset(self) -> None:
        self.collected.clear()
        self.front_queues.clear()
        self.back_queues.clear()
        self.ready_queue.queue.clear()
        self.domain_profiles.clear()
        self.interrupt = Event()
        self.frontier_cv = Condition()
        self.num_threads = None
        self.is_crawling = False

    @staticmethod
    def get_domain(url: str) -> str:
        return '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))


def make_argparser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser(description='run web crawler on Twitter')
    argparser.add_argument('param', help = 'twitter query')
    argparser.add_argument('output_dir', help = 'where to dump data')
    return argparser


if __name__ == '__main__':
    argparser = make_argparser()
    args = argparser.parse_args()
    param: str = args.param
    output_dir = args.output_dir
    target_content_path = osp.join(output_dir, 'content.csv')
    target_url_repo_path = osp.join(output_dir, 'url_repo.txt')

    with (open(target_content_path, "a", encoding="utf-8") as content_f,
            open(target_url_repo_path, 'a') as url_repo_f,
            Timer() as t):
        # TODO add column headers, but need to check if file is new or appending
        content_csv_writer = csv.writer(content_f, quoting=csv.QUOTE_ALL)

        def on_content(url: str, content: list[str], latency: float) -> None:
            for tweet in content:
                content_csv_writer.writerow(tweet)
            url_repo_f.write(f'{url}\n')
            url_repo_f.flush()
            print(f'{round(time.time() - float(t), 2)}: with l={round(latency, 5)}, {thread_id().replace("Thread", "T")} got "{url}"')
        
        # TODO read and pass url_repo to spider
        spider = Spider()
        param = 'soccer'
        seeds = {f'https://twitter.com/search?q={param}'}
        spider.crawl(seeds, on_content)
