"""

"""

import sys
# TODO - Need to fix error causes different import methods required for running API and running normally

#from searchEngine.invertedIndexer import invertedIndex
#from searchEngine.proximity import make_proximity_score_vector

#from searchEngine.rocchio import rocchio
#from searchEngine.tokenizer import tokenize, tokenize_query
#from searchEngine.vectorSpace import cosineSimilarity, createQueryVector, vectorMagnitude, vectorSpace
#sys.path.append('.')


# # -----------------------------------------------------
from invertedIndexer import invertedIndex
from proximity import make_proximity_score_vector

from rocchio import rocchio
from tokenizer import tokenize, tokenize_query
from vectorSpace import cosineSimilarity, createQueryVector, vectorMagnitude, vectorSpace#
sys.path.append('.')
# # -----------------------------------------------------
import os.path as osp, os
import pickle
import argparse
import pandas as pd
from collections import Counter
from icecream import ic

INDEX_COL = "tweet_path"
DATA_DIR = osp.abspath(osp.join(osp.realpath(__file__), os.pardir, os.pardir, 'data'))
CONTENT_PATH = osp.join(DATA_DIR, 'crawlData', 'content.csv')
II_PATH = osp.join(DATA_DIR, "indexes", "IItest.pkl")
VS_PATH = osp.join(DATA_DIR, "indexes", "VStest.pkl")

def cmd_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='IR Twitter Search')
    parser.add_argument('query', help = 'query to search on twitter')
    return parser.parse_args()

def create_Index():
    df = pd.read_csv(CONTENT_PATH, index_col=INDEX_COL)

    # Reset the index to default numbering to drop duplicate tweets
    df.reset_index(inplace=True)
    df.drop_duplicates(subset=[INDEX_COL], inplace=True, keep="first")
    df.set_index(INDEX_COL, inplace=True)
    # Index set back to normal
    tokenizerDf = tokenize(df)
    df.to_csv(CONTENT_PATH)

    tweet_count = len(tokenizerDf.index)
    collection, term_count = invertedIndex(tokenizerDf["tweet"], tweet_count)
    output = open(II_PATH, 'wb')
    pickle.dump(collection, output)
    output.close()
    vs = vectorSpace(collection, term_count, tweet_count)
    output = open(VS_PATH, 'wb')
    pickle.dump(vs, output)
    output.close()

def Search(query, collection, vs):
    # computes cosine similarities
    #Dynamic tasks
    
    # Tokenize query
    queryTokenList = tokenize_query(query)

    term_count = len(vs[0])
    doc_count = len(vs)
    # Create query vector
    queryVector = createQueryVector(queryTokenList, doc_count, collection)

    # Calculate cosine similarities and store in dictionary
    cosSimDictionary = {}
    query_magnitude = vectorMagnitude(queryVector)
    for i in range(len(vs)):
        vector = vs[i]
        if (vector == []):
            print(i)
        cosSimDictionary[i] = cosineSimilarity(vector, queryVector, query_magnitude)
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

    #ic(queryVector, relevant_tweets)
    return queryVector,relevant_tweets

def Vector_Search(query_v, collection, queryTokenList):
    #Dynamic tasks
    vs = pd.read_pickle(f'{DATA_DIR}/indexes/VStest.pkl')  # TODO only read in pickle once

    # Calculate cosine similarities and store in dictionary
    cosSimDictionary = {}
    query_magnitude = vectorMagnitude(query_v)
    for i in range(len(vs)):
        vector = vs[i]
        cosSimDictionary[i] = cosineSimilarity(vector, query_v, query_magnitude)
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

def relevant_user_tweets(relevant_tweets: list[str], irrelevant_tweets: list[str], original_query: list[float], original_query_str: list[str], df, index, vs):
    """Returns new tweets based on relevant tweets provided by the user"""
    # df, index, vs = load_data()
    updated_query_v = rocchio(original_query, relevant_tweets, irrelevant_tweets, df, vs)
    top_n_tweets = Vector_Search(updated_query_v, index, tokenize_query(original_query_str)) #TODO Gather original query token
    list = compile_tweet_list(top_n_tweets, df)
    return list

def API_Query(query : str, df, index, vs) -> tuple[list[float], list]:
    # df, index, vs = load_data()
    query_v, top_n_tweets = Search(query, index, vs)
    list = compile_tweet_list(top_n_tweets, df)
    return (query_v, list)

def load_data():
    # We should only need to read data from here, and 
    df = pd.read_csv(CONTENT_PATH, index_col=INDEX_COL)
    df.reset_index(inplace=True) # Reset the index so that things are simpler
    index = pd.read_pickle(II_PATH)  # TODO only read in pickle once
    vs = pd.read_pickle(VS_PATH)  # TODO only read in pickle once
    return df, index, vs

#create_Index()