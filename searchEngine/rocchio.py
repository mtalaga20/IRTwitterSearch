import pandas as pd
import numpy as np


def rocchio(query_vector, pos_tweet_ids, neg_tweet_ids, df, vs):
    """
    Find vector given tweet_id
    """
    alpha = 1
    beta = 0.5
    c = 0.1

    pos_summation = np.zeros(len(query_vector))
    for i in range(len(pos_tweet_ids)):
        index = df.index[df['tweet_path']==pos_tweet_ids[i]].values
        tweet_vector = vs[index[0]]
        pos_summation += np.array(tweet_vector)

    neg_summation = np.zeros(len(query_vector))
    for i in range(len(neg_tweet_ids)):
        index = df.index[df['tweet_path']==pos_tweet_ids[i]].values
        tweet_vector = vs[index[0]]
        neg_summation += np.array(tweet_vector)

    query_vector = (np.array(query_vector).dot(alpha)) + (pos_summation.dot(beta) - (neg_summation.dot(c)))

    return query_vector