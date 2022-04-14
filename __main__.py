"""

"""
#from copyreg import pickle
import pickle
from gc import collect
from winreg import QueryValue
from tokenizer import tokenize, tokenize_query
from invertedIndexer import invertedIndex
from vectorSpace import cosineSimilarity, createQueryVector, vectorSpace
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
        - stopwords, stemmer, slang?
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
    city = ["Kansas", "Missouri", "Pennsylvania", "New York"]
    for each in city:
        c.Search = 'Jayhawks'
        c.Limit = 100
        c.Lang = "en"
        c.Store_csv = True
        c.Output = "./testfile2.csv"
        #c.Since=...
        #c.Until=...
        #c.Custom = ["date", "tweet", "place"]
        #c.Pandas = True
        c.Near = each
        c.Stats = True
        twint.run.Search(c)
    #Selecting specific columns from pulled data
    #df = twint.output.panda.Tweets_df[["id", "date", "username", "tweet", "place", "hashtags"]]
    #df['date'] = pd.to_datetime(df['date'])
    #df.head()
    #df.info()
    #tokenize(df)
    #tweet_count = len(df.index)
    #collection, term_count = invertedIndex(df["tweet"], tweet_count)
    #print(collection)
    #vs = vectorSpace(collection, term_count, tweet_count)
    #print(vs)
    
def Search(query):
    nest_asyncio.apply()
    c = twint.Config()
    #Parameters
    c.Search = query
    c.Limit = 500
    c.Lang = "en"
    c.Pandas = True
    # Executing Search
    twint.run.Search(c)

    #Selecting specific columns from pulled data
    df = twint.output.panda.Tweets_df[["id", "date", "username", "tweet", "place", "hashtags"]]
    df['date'] = pd.to_datetime(df['date'])
    tokenize(df)
    tweet_count = len(df.index)
    collection, term_count = invertedIndex(df["tweet"], tweet_count)
    output = open('outputs/IItest.pkl', 'wb')
    pickle.dump(collection, output)
    output.close()
    vs = vectorSpace(collection, term_count, tweet_count)
    # Tokenize query
    queryTokenList = tokenize_query(query)

    # Create query vector
    queryVector = createQueryVector(queryTokenList, collection, term_count)

    # Calculate cosine similarities and store in dictionary
    cosSimDictionary = { }
    print(queryVector)
    for i in range(len(vs)):
        vector = vs[i]
        cosSimDictionary[i] = cosineSimilarity(vector, queryVector)
        print(df["tweet"][i])
        print(i)
        print(cosSimDictionary[i])
        # print(vector)
        print()
    print(cosSimDictionary)


def main() -> int:
    args = cmd_line_args()
    query: str = args.query
    #test()
    #test_twint()
    query = "Hello World"
    Search(query)

if __name__ == '__main__':
    main()