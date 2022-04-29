import pandas as pd
import numpy as np
from icecream import ic

def rocchio(query_vector, pos_tweet_ids, neg_tweet_ids, df, vs, alpha, beta, gamma):
    """
    Find vector given tweet_id
    """
    # We send gamma as a positive to simplify front end
    gamma = -1 * gamma

    query_vector = [ (tup_id, tup_val*alpha) for (tup_id, tup_val) in query_vector]

    for i in range(len(pos_tweet_ids)):
        index = df.index[df['tweet_path']==pos_tweet_ids[i]].values
        tweet_vector = vs[index[0]]
        for tuple in tweet_vector:
            query_vector.append((tuple[0], tuple[1] * beta))

    
    for i in range(len(neg_tweet_ids)):
        index = df.index[df['tweet_path']==neg_tweet_ids[i]].values
        tweet_vector = vs[index[0]]
        for tuple in tweet_vector:
            query_vector.append((tuple[0], tuple[1] * gamma))

    return query_vector