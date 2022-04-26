import pandas as pd
import numpy as np
from icecream import ic

def rocchio(query_vector, pos_tweet_ids, neg_tweet_ids, df, vs):
    """
    Find vector given tweet_id
    """
    alpha = 1
    beta = 0.5
    c = -0.1

    for i in range(len(pos_tweet_ids)):
        index = df.index[df['tweet_path']==pos_tweet_ids[i]].values
        tweet_vector = vs[index[0]]
        for tuple in tweet_vector:
            query_vector.append((tuple[0], tuple[1] * beta))

    
    for i in range(len(neg_tweet_ids)):
        index = df.index[df['tweet_path']==pos_tweet_ids[i]].values
        tweet_vector = vs[index[0]]
        for tuple in tweet_vector:
            query_vector.append((tuple[0], tuple[1] * c))

    return query_vector