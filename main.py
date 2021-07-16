# folder = '../codes/dataset/saved/without_phrases/'
from util import *
from esa import ESA, Preprocessing
folder = "./numpy_files/"

phrases = []
abbreviations = {}
with_stemming = 'no'

# course_detail_path = "../codes/dataset/CourseData.csv"
course_detail_path = "./data/course_data.json"

preprocessing = Preprocessing(phrases, abbreviations, with_stemming)
document_content = preprocessing.readDictionary(course_detail_path)
# document_content = preprocessing.readCourseData(course_detail_path)
try:
    wiki_document_esa_matrix = np.load(folder + 'wiki_document_esa_matrix.npy')
    wiki_query_esa_matrix = np.load(folder + 'wiki_query_esa_matrix.npy')
    wiki_esa_similarity_matrix = np.load(folder + 'wiki_esa_similarity_matrix.npy')
    print(wiki_document_esa_matrix)
except:
    # wikipedia_articles_path = "../codes/dataset/QueriedWikipediaArticles/"
    wikipedia_articles_path = "./data/wikipedia.json"

    # base_content = preprocessing.readWikipediaData(wikipedia_articles_path)
    base_content = preprocessing.readDictionary(wikipedia_articles_path)
    # document_content = preprocessing.readCourseData(course_detail_path)
    
    esa = ESA(base_content, document_content, document_content, "same")
    wiki_document_esa_matrix, wiki_query_esa_matrix, wiki_esa_similarity_matrix = esa.computation()
    print(wiki_esa_similarity_matrix.shape)
    np.save(folder + 'wiki_document_esa_matrix.npy', wiki_document_esa_matrix)
    np.save(folder + 'wiki_query_esa_matrix.npy', wiki_query_esa_matrix)
    np.save(folder + 'wiki_esa_similarity_matrix.npy', wiki_esa_similarity_matrix)
    