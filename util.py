import numpy as np
import pandas as pd
import re
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
import spacy
# import string
# from nltk.tokenize import TreebankWordTokenizer
# from nltk.collocations import *
# nltk.download("stopwords")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')

# def remove_punctuation(text):
#     """custom function to remove the punctuation"""
#     PUNCT_TO_REMOVE = string.punctuation + '“' + '”'+'’' + '_'
#     return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

# STOPWORDS = set(stopwords.words('english'))
# def remove_stopwords(text):
#     """custom function to remove the stopwords"""
#     return " ".join([word for word in str(text).split() if word not in STOPWORDS])