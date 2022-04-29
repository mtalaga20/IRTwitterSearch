import re # Regex package
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
# nltk.download('stopwords')
stopwords = stopwords.words('english')
ps = nltk.PorterStemmer() #Porters Stemmer

def tokenize_query(queryString):
    # <TODO> We need to figure out how to deal with something like print(hello)
    #   this is relevant to both querys and documents

    # Replace punctuation
    queryString = re.sub(r"[^a-zA-Z0–9 ]", "", queryString)
    # Split string on SPACES
    queryList = queryString.lower().split(" ")
    # Remove stop words
    i = 0
    while i < len(queryList):
        word = queryList[i]
        if word in stopwords:
            queryList.remove(word)
            continue # skip i + 1 step
        # Apply porter-stemmer if valid
        queryList[i] = ps.stem(word)
        i += 1
    # I feel like the next stop is not necessary because we catch NULL words earlier
    # df.apply(lambda x: [word for word in x if word != " " and word != ""])
    return queryList

def tokenize(df):
    """
    Tokenizer function to take dataframe columns (tweets), and perform tokenizing, stemming,
    :param df:
    :return: modified post-tokenize dataframe
    """
    tDf = df.copy(deep=True)

    #Remove punctuation
    symbols = ["#", "@", "'", ",", ".", '?', "-"]
    tDf["tweet"] = tDf["tweet"].astype(str)
    #tDf["tweet"] = tDf["tweet"].apply(lambda x: x.replace("[^a-zA-Z0-9 ]", ""))
    tDf["tweet"] = tDf["tweet"].str.replace('[^\w\s]','')
    tDf["tweet"] = tDf["tweet"].str.replace('\d+', '')
    #Tokenize
    tDf["tweet"] = tDf["tweet"].apply(lambda x: x.lower().split(" "))
    #Stopwords
    tDf["tweet"] = tDf["tweet"].apply(
        lambda x: [word for word in x if word not in stopwords])
    #Stemmer
    tDf["tweet"] = tDf["tweet"].apply(lambda x: [ps.stem(word) for word in x])
    # Remove empty spots
    tDf["tweet"] = tDf["tweet"].apply(
        lambda x: [word for word in x if word != " " and word != ""])

    # Check for empty spots
    for tweetIndex in tDf.index:
        if (len(tDf.loc[tweetIndex, "tweet"]) == 0):
            print("Dropping: ", tweetIndex)
            # Drop from both the original and the tokenizer df
            df.drop(index=tweetIndex, inplace=True)
            tDf = tDf.drop(index=tweetIndex)
    return tDf
