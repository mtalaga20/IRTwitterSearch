import numpy as np

def invertedIndex(tweets, tweet_count):
    """
    Inverted index that dissects tweets from the dataframe and
    adds the to a sorted collection that has each word and its associated tweet id.
    The collection is added to a dictionary where it further organizes
    the data to be used later for comparison.
    Dictionary = {"Term" : [(df, tf, idf) , [(docID, tf, [indices])...(docID, tf, [indices])]]}
    :param tweets: pandas column that has several tweets
    :param tweet_count: Count of tweets as an int
    :return: Inverted index table as a dictionary
    """
    collection = []
    dictionary = {}
    for i in range(tweet_count):
        tweet = tweets[i]
        index = 0
        for word in tweet:
            collection.append((word, i, index))
            index += 1
    collection = sorted(collection)

    current_term = ""
    prev_docID = -1
    df, tf, dtf = 0, 0, 0
    term_count = 0
    for i in range(len(collection)):
        docID = collection[i][1]
        if collection[i][0] != current_term: #New term
            if current_term != "":#Add previous term to dict
                #dictionary.update({current_term: [(df, tf, (np.log10(tweet_count/df))), new_post]})
                dictionary.update({current_term: new_post})
            df, tf, dtf = 1, 1, 1
            term_count += 1
            current_term = collection[i][0]
            indices = [collection[i][2]]
            new_post = [[docID, tf, indices]]
            
        elif collection[i][0] == current_term and collection[i][1] == prev_docID: #Same term same doc
            dtf += 1
            tf += 1
            new_post.remove([docID, (dtf - 1), indices])
            indices.append(collection[i][2])
            new_post.append([docID, dtf, indices])
        else: #Same term diff doc
            dtf = 1
            tf += 1
            df += 1
            indices = [collection[i][2]] #Index reset
            new_post.append([docID, dtf, indices])
        prev_docID = docID
    return dictionary, term_count