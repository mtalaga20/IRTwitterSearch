"""

"""

from lib2to3.pgen2.tokenize import TokenError
import sys
from searchEngine.invertedIndexer import invertedIndex
from searchEngine.proximity import make_proximity_score_vector

from searchEngine.rocchio import rocchio
from searchEngine.tokenizer import tokenize, tokenize_query
from searchEngine.vectorSpace import cosineSimilarity, createQueryVector, vectorSpace; sys.path.append('.')
import os.path as osp, os
import pickle
import argparse
import pandas as pd
from collections import Counter
from icecream import ic

def cmd_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='IR Twitter Search')
    parser.add_argument('query', help = 'query to search on twitter')
    return parser.parse_args()

def create_Index():
    data_dir = osp.join(osp.realpath(__file__), os.pardir, os.pardir, 'data')
    df = pd.read_csv(f"{data_dir}/crawlData/original_content.csv")
    # df.reset_index(drop=True)
    # df.to_csv(f"{data_dir}/crawlData/original_content.csv")

    tokenize(df)
    tweet_count = len(df.index)
    collection, term_count = invertedIndex(df["tweet"], tweet_count)
    output = open(f'{data_dir}/indexes/IItest.pkl', 'wb')
    pickle.dump(collection, output)
    output.close()
    vs = vectorSpace(collection, term_count, tweet_count)
    output = open(f'{data_dir}/indexes/VStest.pkl', 'wb')
    pickle.dump(vs, output)
    output.close()

def Search(query, collection, vs):
    # computes cosine similarities
    #Dynamic tasks
    
    # Tokenize query
    queryTokenList = tokenize_query(query)

    term_count = len(vs[0])
    # Create query vector
    queryVector = createQueryVector(queryTokenList, collection, term_count)

    # Calculate cosine similarities and store in dictionary
    cosSimDictionary = {}
    for i in range(len(vs)):
        vector = vs[i]
        cosSimDictionary[i] = cosineSimilarity(vector, queryVector)
    cosSimDictionary = Counter(cosSimDictionary)
    k_tweets = 10 #number of relevant tweets to return
    cosSimDictionary = cosSimDictionary.most_common(k_tweets)
    cosSimDictionary = [x for x in cosSimDictionary if x[1] != 0]  # TODO find candidate docs before computing cosine sim
    candidates = [tuple[0] for tuple in cosSimDictionary]
    filtered_queryterms = sorted(queryTokenList)
    filtered_queryterms = [word for word in filtered_queryterms if word in collection] #Remove word if they never appear in collection
    proximity_vector = make_proximity_score_vector(collection, filtered_queryterms, candidates)

    #Add promiximity to cos-sim scores
    relevant_tweets = []
    cos_weight, proxim_weight = 1.0, 0.2
    for i in range(len(cosSimDictionary)):
        relevant_tweets.append((cosSimDictionary[i][0], ((cosSimDictionary[i][1] * cos_weight) + (proximity_vector[i] * proxim_weight))))

    return queryVector,relevant_tweets

def Vector_Search(query_v, collection, queryTokenList):
    #Dynamic tasks
    data_dir = osp.join(osp.realpath(__file__), os.pardir, os.pardir, 'data')
    vs = pd.read_pickle(f'{data_dir}/indexes/VStest.pkl')  # TODO only read in pickle once

    # Calculate cosine similarities and store in dictionary
    cosSimDictionary = {}
    for i in range(len(vs)):
        vector = vs[i]
        cosSimDictionary[i] = cosineSimilarity(vector, query_v)
    cosSimDictionary = Counter(cosSimDictionary)
    k_tweets = 10  # number of relevant tweets to return
    cosSimDictionary = cosSimDictionary.most_common(k_tweets)
    cosSimDictionary = [x for x in cosSimDictionary if x[1] != 0]  # TODO find candidate docs before computing cosine sim
    candidates = [tuple[0] for tuple in cosSimDictionary]
    filtered_queryterms = sorted(queryTokenList)
    filtered_queryterms = [word for word in filtered_queryterms if word in collection] #Remove word if they never appear in collection
    proximity_vector = make_proximity_score_vector(collection, filtered_queryterms, candidates)

    #Add promiximity to cos-sim scores
    relevant_tweets = []
    cos_weight, proxim_weight = 1.0, 0.2
    for i in range(len(cosSimDictionary)):
        relevant_tweets.append((cosSimDictionary[i][0], ((cosSimDictionary[i][1] * cos_weight) + (proximity_vector[i] * proxim_weight))))

    return relevant_tweets

def compile_tweet_list(relevant_tweets, df):
    tweet_list = []
    for i in range(len(relevant_tweets)):
        rank = i+1
        uri = df['tweet_path'][relevant_tweets[i][0]]
        tweet = df["tweet"][relevant_tweets[i][0]]
        tweet_list.append((rank, uri, tweet))
    return tweet_list

def relevant_user_tweets(relevant_tweets: list[str], irrelevant_tweets: list[str], original_query: list[float], original_query_str: list[str]):
    """Returns new tweets based on relevant tweets provided by the user"""
    df, index, vs = load_data()
    updated_query_v = rocchio(original_query, relevant_tweets, irrelevant_tweets, df, vs)
    top_n_tweets = Vector_Search(updated_query_v, index, tokenize_query(original_query_str)) #TODO Gather original query token
    list = compile_tweet_list(top_n_tweets, df)
    return list

def API_Query(query : str) -> tuple[list[float], list]:
    # We need a way to ensure the index has been created before this so it does not run every time

    # create_Index()
    #For loading csv:
    df, index, vs = load_data()
    query_v, top_n_tweets = Search(query, index, vs)
    list = compile_tweet_list(top_n_tweets, df)
    return (query_v, list)

# def search(query: str, relevant_doc_ids) -> int:
#     create_Index()
#     #For loading csv:
#     df, index, vs = load_data()
#     query_v, top_n_tweets = Search(query, index, vs)
#     list = compile_tweet_list(top_n_tweets, df)
#     return list

def load_data():
    data_dir = osp.join(osp.realpath(__file__), os.pardir, os.pardir, 'data')
    df = pd.read_csv(f"{data_dir}/crawlData/original_content.csv")
    # df.reset_index(drop=True)
    # df.to_csv(f"{data_dir}/crawlData/original_content.csv")
    index = pd.read_pickle(osp.abspath(osp.join(osp.realpath(__file__), os.pardir, os.pardir, 'data', 'indexes', 'IItest.pkl')))  # TODO only read in pickle once
    vs = pd.read_pickle(osp.abspath(osp.join(osp.realpath(__file__), os.pardir, os.pardir, 'data', 'indexes', 'VStest.pkl')))  # TODO only read in pickle once
    return df, index, vs

# search('hello spotted eagle magic internet money', 2)