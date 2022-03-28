def vectorSpace(invertedIndex, term_count, doc_count):
    """
    Vector space function to create weights for each term in respect to each document.
    Weights calculated by the term's idf multiplied by the doc's respective term frequency.
    :param invertedIndex: Dictionary featuring each term's associated term frequency,
    doc frequency, inverse-doc frequency,and a list of the postings list
    :param term_count: Integer for the number of unique terms
    :param doc_count: Integer for the number of tweets
    :return: 2D list of the vector space for the documents (list of floats)
    """
    # Vector space dimensions: doc_count x term_count
    vector_space = [[0 for i in range(term_count)] for i in range(doc_count)]
    term_position = 0
    for term, values in invertedIndex.items():
        idf = values[0][2]
        for doc in values[1]: #Update positions in vector space
            docID, tf = doc[0], doc[1]
            vector_space[docID][term_position] = idf * tf
        term_position += 1
    return vector_space

def createQueryVector(queryList, invertedIndex, term_count):
    """
    :param queryList: List of tokens making up query (post-tokenizing)
    :param invertedIndex: 
    :param term_count: Integer for number of unique terms
        # NOTE: Maybe we can replace with len(term_idf_dict)?
    :return: Vector 1 x (term_count) size representing the query
    """

    vector = [0 for _ in range(term_count)]

    term_pos = 0
    for term, values in invertedIndex.items():
        idf = values[0][2]
        for word in queryList:
            if word == term:
                vector[term_pos] = vector[term_pos] + idf
        term_pos += 1
    return vector

def vectorMagnitude(vector):
    sum = 0
    for i in range(len(vector)):
        sum += vector[i]**2
    return (sum**0.5)

def cosineSimilarity(doc_vector, query_vector):
    doc_magnitude = vectorMagnitude(doc_vector)
    query_magnitude = vectorMagnitude(query_vector)
    numerator = 0

    # Foreach value in vector take query[i] * doc[i]
    for i in range(len(doc_vector)):
        # NOTE: Possible optimization here for 0 values?
        numerator += doc_vector[i] * query_vector[i]
    
    return (numerator / (doc_magnitude * query_magnitude))