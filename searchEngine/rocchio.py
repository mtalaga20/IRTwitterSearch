import pandas as pd
import numpy as np


def rocchio(query_vector, tweet_ids):
    """
    Find vector given tweet_id
    """
    alpha = 1
    beta = 0.5
    vs = pd.read_pickle(r'outputs/VStest.pkl')
    df = pd.read_csv("crawlData/output.csv")
    print(tweet_ids)
    summation = np.zeros(len(query_vector))
    for i in range(len(tweet_ids)):
        index = df.index[df['tweet_path']==tweet_ids[i][1]].values
        print(index)
        tweet_vector = vs[index[0]]
        summation += np.array(tweet_vector)

    query_vector = (np.array(query_vector).dot(alpha)) + (summation.dot(beta))

    return query_vector