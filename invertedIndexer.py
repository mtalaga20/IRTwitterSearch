
def merge(collection):
    """

    :param collection:
    :return: list of tuples with word and doc id
    """
    #for i in range(len(collection)):
        #for j in range()
def invertedIndex(df):
    """

    :param df:
    :return: Inverted index table as a dictionary
    """
    collection = []
    for i in range(df.shape[0]):
        tweet = df.loc[i]["tweet"]
        for word in tweet:
            collection.append((word, i))
    return sorted(collection)