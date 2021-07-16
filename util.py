import numpy as np
import pandas as pd
import re, os, json, math
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
import spacy
                                          
from nltk.tokenize import word_tokenize                       
from nltk.corpus import stopwords                             
from sklearn.feature_extraction.text import TfidfVectorizer   
import scipy.sparse                                         
from sklearn.metrics.pairwise import cosine_similarity        
from nltk.stem import PorterStemmer
from esa import *
nltk.download('stopwords')
nltk.download('punkt')

# import string
# from nltk.tokenize import TreebankWordTokenizer
# from nltk.collocations import *
# nltk.download("stopwords")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')


def read_dictionary(path):
    content = {}
    data = json.load(open(path, "r", encoding="utf-8"))
    content = data
    return content

def calculate_relatedness(esa_w, book_simi_w, course_detail_path, course):
    esa_simi_matrix = run_esa()
    book_simi_matrix = np.identity(len(esa_simi_matrix))

    data_dict = read_dictionary(course_detail_path)
    data_list = list(data_dict)
    index = list(data_dict).index(course)
    # print(index)
    # print(esa_simi_matrix[index])
    # print(book_simi_matrix[index])
    convex_result = ((float(esa_w)*np.array(esa_simi_matrix[index])) + (float(book_simi_w)*np.array(book_simi_matrix[index])))/float(esa_w+book_simi_w)
    print(esa_simi_matrix[index])
    print(esa_simi_matrix)
    print(np.count_nonzero(esa_simi_matrix))
    order = np.argsort(-convex_result)
    print(order)
    related_courses = dict()
    
    for i in range(10):
        related_courses[data_list[order[i]]] = convex_result[order[i]]
    return related_courses