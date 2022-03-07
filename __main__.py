"""

"""

import argparse
from email import header
from icecream import ic
import datetime as DT
import pandas as pd
import numpy as np
from Scweet.scweet import scrape
from Scweet.user import get_user_information, get_users_following, get_users_followers


def cmd_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='IR Twitter Search')
    parser.add_argument('query', help = 'query to search on twitter')
    return parser.parse_args()


def test():
    #Short period of time for testing
    day_ago = DT.date.today() - DT.timedelta(days = 1)

    '''
    Data is a pandas dataframe that consists of tweets and
    and their associated information like username, timestamp, likes, and comments.
    '''
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
        geocode = '38.3452,-0.481006,20km'  # within this geographic region
    )
    
    #Cleaning
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    print(data.info())
    '''
    Next steps:
    1. Gather unique words from tweets (unsure if posting list is needed)
    2. Sort unique words
    3. Create idf values for each word
    4. Create weights for each document, append to its respective row in data?
    5. Be able to accept a query and create weights similar to document
        - Thinking first query will be a category or buzz word, and 2nd query will be a more narrow search.
        - Example: Category = Cryptocurrency , query = "Is bitcoin going to go up in price in April?"
        - This allows a smaller set of tweets given by the category.
    6. Compute cosine similarity between query and tweets  
    7. Return n tweets
    '''
  


def main() -> int:
    args = cmd_line_args()
    query: str = args.query
    test()

if __name__ == '__main__':
    main()