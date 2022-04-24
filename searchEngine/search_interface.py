import pickle
from searchEngine.rocchio import rocchio
from searchEngine.tokenizer import tokenize, tokenize_query
from searchEngine.invertedIndexer import invertedIndex
from searchEngine.vectorSpace import cosineSimilarity, createQueryVector, vectorSpace
import argparse
import pandas as pd
from collections import Counter


def cmd_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='IR Twitter Search')
    parser.add_argument('query', help = 'query to search on twitter')
    return parser.parse_args()

def create_Index():
    #Selecting specific columns from pulled data
    #For loading csv:
    data_dir = "crawlData"
    df = pd.read_csv(f"{data_dir}/output.csv")
    df.reset_index(drop=True)
    df.to_csv(f"{data_dir}/output.csv") 

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

def Search(query):

    #Dynamic tasks
    collection = pd.read_pickle(r'outputs/IItest.pkl')
    vs = pd.read_pickle(r'outputs/VStest.pkl')
    # Tokenize query
    queryTokenList = tokenize_query(query)

    term_count = len(vs[0])
    # Create query vector
    queryVector = createQueryVector(queryTokenList, collection, term_count)

    # Calculate cosine similarities and store in dictionary
    cosSimDictionary = { }
    for i in range(len(vs)):
        vector = vs[i]
        cosSimDictionary[i] = cosineSimilarity(vector, queryVector)
    cosSimDictionary = Counter(cosSimDictionary)
    k_tweets = 10 #number of relevant tweets to return
    cosSimDictionary = cosSimDictionary.most_common(k_tweets)
    cosSimDictionary = [x for x in cosSimDictionary if x[1] != 0]
    return queryVector, cosSimDictionary

def Vector_Search(query_v):
    #Dynamic tasks
    vs = pd.read_pickle(r'outputs/VStest.pkl')

    # Calculate cosine similarities and store in dictionary
    cosSimDictionary = {}
    for i in range(len(vs)):
        vector = vs[i]
        cosSimDictionary[i] = cosineSimilarity(vector, query_v)
    cosSimDictionary = Counter(cosSimDictionary)
    k_tweets = 10  # number of relevant tweets to return
    cosSimDictionary = cosSimDictionary.most_common(k_tweets)
    cosSimDictionary = [x for x in cosSimDictionary if x[1] != 0]
    return query_v, cosSimDictionary

def compile_tweet_list(relevant_tweets):
    data_dir = "crawlData"
    df = pd.read_csv(f"{data_dir}/output.csv")
    tweet_list = []
    for i in range(len(relevant_tweets)):
        rank = i+1
        uri = df['tweet_path'][relevant_tweets[i][0]]
        tweet = df["tweet"][relevant_tweets[i][0]]
        tweet_list.append((rank, uri, tweet))
    return tweet_list

def relevant_user_tweets(relevant_tweets, original_query):
    """Returns new tweets based on relevant tweets provided by the user"""
    updated_query_v = rocchio(original_query, relevant_tweets)
    query_v, top_n_tweets = Vector_Search(updated_query_v)
    list = compile_tweet_list(top_n_tweets)
    return list

def search(query: str, relevant_doc_ids) -> int:
    create_Index()
    query_v, top_n_tweets = Search(query)
    list = compile_tweet_list(top_n_tweets)
    return list
