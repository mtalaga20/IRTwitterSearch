"""

"""

from tokenizer import tokenize
from invertedIndexer import invertedIndex
import argparse
from email import header
from icecream import ic
import datetime as DT
import pandas as pd
import numpy as np
from Scweet.scweet import scrape
from Scweet.user import get_user_information, get_users_following, get_users_followers
import twint
import nest_asyncio

'''
    Next steps:
    0.1. Tokenize words
        - stopwords, stemmer
    1. Gather unique words from tweets (create inverted index + posting list)
    2. Sort unique words
    3. Create idf values for each word
    4. Create weights for each document, append to its respective row in data?
    5. Be able to accept a query and create weights similar to document
        - Thinking first query will be a category or buzz word, and 2nd query will be a more narrow search.
            - Alternative could be location?
        - Example: Category = Cryptocurrency , query = "Is bitcoin going to go up in price in April?"
        - This allows a smaller set of tweets given by the category.
    6. Compute cosine similarity between query and tweets  
    7. Return n tweets
'''

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
  
def test_twint():
    '''
    Twint search based on a keyword, it pulls a certain amount of tweets set by the limit.
    :return: N/A
    '''
    nest_asyncio.apply()
    c = twint.Config()
    #Parameters
    c.Search = 'keyword'
    c.Limit = 5
    c.Lang = "en"
    #c.Since=...
    #c.Until=...
    #c.Custom = ["date", "tweet", "place"]
    c.Pandas = True
    twint.run.Search(c)
    #Selecting specific columns from pulled data
    df = twint.output.panda.Tweets_df[["id", "date", "username", "tweet", "place", "hashtags"]]
    df['date'] = pd.to_datetime(df['date'])
    df.head()
    df.info()
    tokenize(df)
    print(df.loc[0:5]["tweet"])
    collection = invertedIndex(df)
    print(collection)




def main() -> int:
    args = cmd_line_args()
    query: str = args.query
    #test()
    test_twint()

if __name__ == '__main__':
    main()