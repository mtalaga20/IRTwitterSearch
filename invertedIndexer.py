
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
    dictionary = {}
    for i in range(df.shape[1]):
        tweet = df.loc[i]["tweet"]
        for word in tweet:
            collection.append((word, i))
    collection = sorted(collection)
    #Dictionary = { "Term" : [(df, tf) , [(docID, tf)...(docID, tf)]]}


    current_term = ""
    prev_docID = -1
    df, tf, dtf = 0, 0, 0
    for i in range(len(collection)):
        docID = collection[i][1]
        if collection[i][0] != current_term: #New term
            if current_term != "":#Add previous term to dict
                dictionary.update({current_term: [(df, tf), new_post]})
            df, tf, dtf = 1, 1, 1
            current_term = collection[i][0]
            #docID, prev_docID = collection[i][1], collection[i][1]
            new_post = [[docID, tf]]
            #Term is not adding to posting list
        elif collection[i][0] == current_term and collection[i][1] == prev_docID: #Same term same doc
            dtf += 1
            tf += 1
            new_post.remove([docID, (dtf - 1)])
            new_post.append([docID, dtf])
        else: #Same term diff doc
            dtf = 1
            tf += 1
            df += 1
            new_post.append([docID, dtf])
        if i == len(collection):
            dictionary.update({current_term : [(df, (tf + dtf)), new_post]})
        prev_docID = docID
    return dictionary