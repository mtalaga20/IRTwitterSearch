import pandas as pd
import numpy as np


def rocchio(query_vector, tweet_ids, df, vs):
    """
    Find vector given tweet_id
    """
    alpha = 1
    beta = 0.5

    summation = np.zeros(len(query_vector))
    for i in range(len(tweet_ids)):
        index = df.index[df['tweet_path']==tweet_ids[i]].values
        tweet_vector = vs[index[0]]
        summation += np.array(tweet_vector)

    query_vector = (np.array(query_vector).dot(alpha)) + (summation.dot(beta))

    return query_vector