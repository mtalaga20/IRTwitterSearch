"""

"""
#from copyreg import pickle
import pickle
from gc import collect
from winreg import QueryValue
from searchEngine.tokenizer import tokenize, tokenize_query
from searchEngine.invertedIndexer import invertedIndex
from searchEngine.vectorSpace import cosineSimilarity, createQueryVector, vectorSpace
import argparse
from email import header
from icecream import ic
import datetime as DT
import pandas as pd
import numpy as np

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

def create_Index():
    #Selecting specific columns from pulled data
    #For loading csv:
    data_dir = "crawlData"
    df = pd.read_csv(f"{data_dir}/output.csv")

    #df['date'] = pd.to_datetime(df['date'])
    tokenize(df)
    tweet_count = len(df.index)
    collection, term_count = invertedIndex(df["tweet"], tweet_count)
    output = open('outputs/IItest.pkl', 'wb')
    pickle.dump(collection, output)
    output.close()
    vs = vectorSpace(collection, term_count, tweet_count)
    output = open('outputs/VStest.pkl', 'wb')
    pickle.dump(vs, output)
    output.close()
    print(term_count)

def Search(query):

    #Dynamic tasks
    collection = pd.read_pickle(r'outputs/IItest.pkl')
    vs = pd.read_pickle(r'outputs/VStest.pkl')
    # Tokenize query
    queryTokenList = tokenize_query(query)

    # Create query vector
    queryVector = createQueryVector(queryTokenList, collection, 494)
    #queryVector = createQueryVector(queryTokenList, collection, term_count)

    # Calculate cosine similarities and store in dictionary
    cosSimDictionary = { }
    print(queryVector)
    for i in range(len(vs)):
        vector = vs[i]
        cosSimDictionary[i] = cosineSimilarity(vector, queryVector)
        #print(i)
        #print(cosSimDictionary[i])
        # print(vector)
        print()
    print(cosSimDictionary)


def main() -> int:
    args = cmd_line_args()
    query: str = args.query
    query = "Hello World"
    #create_Index()
    Search(query)

if __name__ == '__main__':
    main()