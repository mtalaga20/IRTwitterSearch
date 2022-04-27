"""

"""

from icecream import ic


def vectorSpace(invertedIndex, term_count, doc_count):
    """
    Vector space function to create weights for each term in respect to each document.
    Weights calculated by the term's idf multiplied by the doc's respective term frequency.
    :param invertedIndex: Dictionary featuring each term's associated term frequency,
    doc frequency, inverse-doc frequency,and a list of the postings list
    VS = [[(termID, weight)][(termID, weight), (termID, weight)]] #as many lists as there are tweets
    :param term_count: Integer for the number of unique terms
    :param doc_count: Integer for the number of tweets
    :return: 2D list of the vector space for the documents (list of floats)
    """
    # Vector space dimensions: doc_count x term_count
    vector_space = [[] for i in range(doc_count)] #empty list
    term_position = 0
    for term, values in invertedIndex.items():
        idf = values[0][2]
        for doc in values[1]: #Update positions in vector space
            docID, tf = doc[0], doc[1]
            weight = idf * tf
            if weight > 0:
                vector_space[docID].append((term_position, weight))
        term_position += 1
    return vector_space

def createQueryVector(queryList, invertedIndex):
    """
    Structure: [(termID, weight) for each word in query]
    :param queryList: List of tokens making up query (post-tokenizing)
    :param invertedIndex: Index of terms as dict
        # NOTE: Maybe we can replace with len(term_idf_dict)?
    :return: Vector 1 x (query_term_count) size representing the query
    """

    vector = []

    term_pos = 0
    for term, values in invertedIndex.items():
        idf = values[0][2]
        for word in queryList:
            if word == term:
                vector.append((term_pos, idf))
        term_pos += 1
    return vector

def vectorMagnitude(vector):
    sum = 0
    for i in range(len(vector)):
        sum += vector[i][1]**2
    return (sum**0.5)

def cosineSimilarity(doc_vector, query_vector, query_magnitude):
    doc_magnitude = vectorMagnitude(doc_vector)
    #query_magnitude = vectorMagnitude(query_vector)
    numerator = 0

    # Foreach value in vector take query[i] * doc[i]
    for i in range(len(query_vector)):
        # NOTE: Possible optimization here for 0 values?
        term_index = query_vector[i][0]
        
        for j in range(len(doc_vector)):
            
            if term_index == doc_vector[j][0]:
                numerator += doc_vector[j][1] * query_vector[i][1]
            #else continue

    return (numerator / (doc_magnitude * query_magnitude))