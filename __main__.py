"""

"""

import argparse
from email import header
from icecream import ic
import datetime as DT
import pandas as pd
from Scweet.scweet import scrape
from Scweet.user import get_user_information, get_users_following, get_users_followers


def cmd_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='IR Twitter Search')
    parser.add_argument('query', help = 'query to search on twitter')
    return parser.parse_args()


def test():
    #Short period of time for testing
    day_ago = DT.date.today() - DT.timedelta(days = 1)

    data = scrape(
        words = ['bitcoin', 'ethereum'],  # tweets (or other?) containing these terms?
        since = str(day_ago),
        # until = '2021-2-27',  # defaults to today
        from_account = None,
        interval = 1,
        headless = False,
        display_type = 'Top',
        save_images = False,
        lang = 'en',
	    resume = False,
        filter_replies = False,
        proximity = False,
        geocode = '38.3452,-0.481006,200km'  # within this geographic region
    )
    
    #df = pd.DataFrame(data)
    print(data)
    #print(df)


def main() -> int:
    args = cmd_line_args()
    query: str = args.query
    test()

if __name__ == '__main__':
    main()