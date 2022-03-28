def vectorSpace(invertedIndex, term_count, doc_count):
    """

    :param invertedIndex:
    :param term_count: Integer for the number of unique terms
    :return:
    """
    # Vector space dimensions: doc_count x term_count
    vector_space = [[0 for i in range(term_count)] for i in range(doc_count)]
    #print(f"Term {term_count} \nDoc {doc_count}")
    #print(vector_space)
    term_position = 0
    for term, values in invertedIndex.items():
        idf = values[0][2]
        #print(term[0], values, len(vector_space), doc_count , len(vector_space[0]))
        for doc in values[1]: #Update positions in vector space
            docID, tf = doc[0], doc[1]
            #print(docID, tf)
            vector_space[docID][term_position] = idf * tf
        term_position += 1
    return vector_space


def queryVector(query_data_frame, term_idf_dict, term_count):
    """
    :param query_data_frame: Data frame for query (post-tokenizing)
    :param term_idf_dict: Dictionary mapping term-> idf ( "Term": IDF , ...)
    :param term_count: Integer for number of unique terms
        # NOTE: Maybe we can replace with len(term_idf_dict)?
    :return: Vector 1 x (term_count) size representing the query
    """

    vector = [0 for i in range(term_count)]

    term_pos = 0
    for word in query_data_frame["tweet"]:
        if word in term_idf_dict:
            # Position = old value (in case duplicate words in query) + idf * 1 
            #               The use of old value makes idf * 1 work
            vector[term_pos] = vector[term_pos] + term_idf_dict[word]
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