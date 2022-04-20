"""
Solution to Problem 4
"""

import pandas as pd
import numpy as np
import re

df = pd.read_excel(r"Problem_4_Dataset.xlsx")
print(f"The data has {df.shape[0]} Rows and {df.shape[1]} Columns.")

df['FORMATTED_ADDRESS'] = df['FORMATTED_ADDRESS'].str.lower()
df["Location_ID"] = df.index
df = df[['Location_ID', "FORMATTED_ADDRESS", "LOCALITY"]]


def clean_address(address):
    """
    This function will do the following text processing:
    1. Translate text if not in english
    1. Remove Stopwords, using nltk's english stopwords.
    2. Remove Punctuations, using punctuations from string library.
    3. Return a list of cleaned address.
    """
    punctuations = "!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~"
    #address = translator.translate(address, src ='hi',dest='en').text # text from hi is to be converted to english.
    address = re.sub(r'\d+', '', address)
    address = [word.strip() for word in ("".join([char for char in address if char not in punctuations])).split(",")]

    return [word for word in address if word != '']


def clean_address_to_df(address):
    """
    This function will do the following text processing:
    1. Translate text if not in english
    1. Remove Stopwords, using nltk's english stopwords.
    2. Remove Punctuations, using punctuations from string library.
    3. Return a list of cleaned address.
    """
    punctuations = "!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~"
    #address = translator.translate(address, src ='hi',dest='en').text
    address = re.sub(r'\d+','', address)
    address = [word.strip() for word in ("".join([char for char in address if char not in punctuations])).split(",")]
    return ",".join([word for word in address if word !=''])


df['List_of_WordsinSent'] = df['FORMATTED_ADDRESS'].apply(lambda x: clean_address(x))
df['Cleaned_ADD'] = df['FORMATTED_ADDRESS'].apply(lambda x: clean_address_to_df(x))


def term_freq(word, i):
    """
    TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
    """
    document_word_freq = df['List_of_WordsinSent'][i].count(word) # number of times a word appears in a document.
    #document_word_count #This variable will be assigned a value in the loop.
    tf = document_word_freq/document_word_count
    return tf

def idf(word, i):
    """
    IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
    """
    total_no_document = len(df['List_of_WordsinSent'])
    no_document_with_word = df['Cleaned_ADD'].str.contains(word).sum()
    idf = np.log(total_no_document/no_document_with_word) # log base 10
    return idf


result = pd.DataFrame()
for i in range(len(df['List_of_WordsinSent'][:50])):  # for less computation purpose, only few addresses are considered.
    document_word_count = len(df['List_of_WordsinSent'][i])  # storing total no. of word in the document.
    for word in df['List_of_WordsinSent'][i]:
        result = result.append({"Word": word,
                                "Location_ID": df['Location_ID'][i],
                                "Location_Name": df['LOCALITY'][i],
                                "Term_Frequency_(TF)": term_freq(word, i),
                                "Inverse_Document_Frequency_(IDF)": idf(word, i)}, ignore_index=True)
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 10)
print(result)