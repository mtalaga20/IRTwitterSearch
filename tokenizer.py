import pandas as pd
import re # Regex package
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = stopwords.words('english')
ps = nltk.PorterStemmer() #Porters Stemmer

def tokenize_query(queryString):
    # Replace punctuation
    queryString = re.sub(r"[^a-zA-Z0–9 ]", "", queryString)
    # Split string on SPACES
    queryList = queryString.lower().split(" ")
    # Remove stop words
    i = 0
    while i < len(queryList):
        print(i, queryList)
        word = queryList[i]
        if word in stopwords:
            queryList.remove(word)
            continue # skip i + 1 step
        # Apply porter-stemmer if valid
        queryList[i] = ps.stem(word)
        i += 1
    # I feel like the next stop is not necessary because we catch NULL words earlier
    # df.apply(lambda x: [word for word in x if word != " " and word != ""])
    return pd.DataFrame(queryList)

def tokenize(df):
    """
    Tokenizer function to take dataframe columns (tweets), and perform tokenizing, stemming,
    :param df:
    :return:
    """

    #Remove punctuation
    df["original_tweet"] = df["tweet"]
    df["tweet"] = df["tweet"].str.replace("[^a-zA-Z0–9 ]", "")
    #Tokenize
    df["tweet"] = df["tweet"].apply(lambda x: x.lower().split(" "))
    #Stopwords
    df["tweet"] = df["tweet"].apply(lambda x: [word for word in x if word not in stopwords])
    #Stemmer
    df["tweet"] = df["tweet"].apply(lambda x: [ps.stem(word) for word in x])
    # Remove empty spots
    df["tweet"] = df["tweet"].apply(lambda x: [word for word in x if word != " " and word != ""])