

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = stopwords.words('english')
ps = nltk.PorterStemmer() #Porters Stemmer

def tokenize(df):
    """

    :return:
    """

    #Remove punctuation
    df["tweet"] = df["tweet"].str.replace("[^a-zA-Z0–9 ]", "")
    #Tokenize
    df["tweet"] = df["tweet"].apply(lambda x: x.lower().split(" "))
    #Stopwords
    df["tweet"] = df["tweet"].apply(lambda x: [word for word in x if word not in stopwords])
    #Stemmer
    df["tweet"] = df["tweet"].apply(lambda x: [ps.stem(word) for word in x])
    #Remove empty spots
    df["tweet"] = df["tweet"].apply(lambda x: [word for word in x if word != " "])