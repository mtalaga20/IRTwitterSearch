

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

def tokenize(df):
    """

    :return:
    """

    #Remove punctuation
    df["tweet"] = df["tweet"].str.replace("[^a-zA-Z0–9 ]", "")
    #Tokenize
    df["tweet"] = df["tweet"].apply(lambda x: x.lower().split(" "))