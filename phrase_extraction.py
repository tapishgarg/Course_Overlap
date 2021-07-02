# from util import *
from keybert import KeyBERT

def phrase_extractor(doc):
    model = KeyBERT("distilbert-base-nli-mean-tokens")
    keywords = model.extract_keywords(doc, keyphrase_ngram_range=(1,2), stop_words='english', nr_candidates=20, top_n=5)
    return keywords

# doc = """
#          History of aviation and space flight; Classification of aircraft and space vehicles; Functions of major components of airplane and space vehicles;
#          subdivisions of aerospace engineering; elements of aerodynamics, propulsion, structures, systems, flight mechanics and controls.  Indian aerospace
#          activities. Scientific document preparation, report writing and standardization; Graphing Techniques; basic scientific computing, statistical 
#          treatment of data and curve fitting.
#       """

# print(phrase_extractor(doc))