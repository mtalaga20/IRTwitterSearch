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
#def queryVector(query, )