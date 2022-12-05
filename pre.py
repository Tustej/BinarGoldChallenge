
import pandas as pd
import nltk
import re

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from datetime import datetime
#import matplotlib.pyplot as plt
#from PIL import Image
#import seaborn as sns
#from nltk.util import ngrams
#from collections import defaultdict

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

import numpy as np
import os


def data_cleaning(text):
    html_tag = re.compile(r'<.*?>')
    text = re.sub(html_tag, r'', text)

    http_link = re.compile(r'https://\S+')
    www_link = re.compile(r'www\.\S+')
    
    text = re.sub(http_link, r'', text)
    text = re.sub(www_link, r'', text)

    punctuation = re.compile(r'[^\w\s]')
    text = re.sub(punctuation, r'', text)

    return text

def remove(Tweet):
    #hapus rt
    Tweet = re.sub(r'^RT[\s]+', '', Tweet)
    #hapus user
    Tweet = re.sub('USER', '',Tweet)
    #hapus angka
    Tweet = re.sub('[0-9]+', '', Tweet)
    #hapus symbol
    Tweet = re.sub(r'\$\w*', '', Tweet)
    return Tweet


#fungsi preprocessing
def prepros (data, name_column_dataset):
    data[name_column_dataset] = data[name_column_dataset].apply(lambda x: x.lower())
    data['Tweet'] = data['Tweet'].apply(lambda x:remove(x))
    data["remove_punc"] = data[name_column_dataset].apply(lambda x: data_cleaning(x))
    data["clean"] = data["remove_punc"].apply(lambda x: word_tokenize(x))

    start = datetime.now()
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    data["clean"] = data["clean"].apply(lambda x: " ".join(stemmer.stem(word) for word in x))
    end_stem = datetime.now()
    print ("stemmer done",(start-end_stem))

    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    data["clean"] = data["clean"].apply(lambda x: " ".join(stopword.remove(x) for x in x.split()))
    end_stop = datetime.now()
    print ("stopword done", (end_stop - end_stem))
    
    data["clean"] = data["clean"].apply(lambda x:re.sub(' +', ' ',x))

    return(data)