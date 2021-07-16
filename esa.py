from util import *

class Preprocessing:
    
    def __init__(self, phrases, abbreviation, with_stemming):
        self.stop_words = list(set(stopwords.words('english')))
        self.common_word = ['introduction', 'overview', 'basic', 'various', 'topics', 'review', 'course', 'student', 'content', 'academic', 'necessary', 'different']
        self.stop_words = self.stop_words + self.common_word
        self.phrases = phrases
        self.abbreviations = abbreviation
        self.with_stemming = with_stemming

        
    def cleanData(self, text):
        """
            Input   : text to be cleaned.
            Returns : cleaned text string.
        """
        text = text.replace("'"," ").replace("\""," ").replace(";"," ").replace(","," ").replace("-"," ").replace(":"," ").replace("["," ").replace("]"," ").replace("."," ").replace("/"," ").lower()
        text = word_tokenize(text)
        if self.with_stemming == 'yes':
            ps = PorterStemmer()
            text = [ps.stem(token) for token in text if (token.replace('_', '').isalnum() and not token.replace('_', '').isnumeric() and token not in self.stop_words and len(token)>1) ]
        else:
            text = [token for token in text if (token.replace('_', '').isalnum() and not token.replace('_', '').isnumeric() and token not in self.stop_words and len(token)>1) ]
        return " ".join(text)
    
    def phrase_replacement(self, intext):
        outtext = intext
        for phrase in self.phrases:
            phrase_ = phrase.replace("_", " ")
            if phrase_ in outtext.lower():
                outtext = outtext.lower().replace(" "+phrase_+" ", " "+phrase+" ")
        return outtext
    
    
    def abbreviation_replacement(self, intext):
        outtext = intext
        for abbreviation in self.abbreviations:
            if abbreviation in outtext:
                outtext = outtext.replace(" "+abbreviation+" ", " "+abbreviation+" "+self.abbreviations[abbreviation]+" ")
            elif self.abbreviations[abbreviation] in outtext:
                outtext = outtext.replace(" "+self.abbreviations[abbreviation]+" ", " "+abbreviation+" "+self.abbreviations[abbreviation]+" ")
        return outtext
    

    def readWikipediaData(self, base_directory):
        """
            Input   : directory path.
            Returns : Wikipedia article titles and contents ordered list.
        """
        files = os.listdir(base_directory)
        content = {}

        for file in files:
            file_path = base_directory + file
            data = json.load(open(file_path,"r",encoding="utf-8"))
            for title in data['pages']:
                details = data['pages'][title]['text'] + ' ' + title
                details = self.cleanData(details)
                content[title] = self.phrase_replacement(self.abbreviation_replacement(details))
        return content


    def readCourseData(self, document_filename):
        """
            Input   : File path.
            Returns : Course titles and Course details ordered list.
        """
        df = pd.read_csv(document_filename)
        content = {}
        for index,row in df.iterrows():
            details = row['description']+' '+row['content'] +' ' +row['coursename']
            details = self.cleanData(details)
            course_detail = self.phrase_replacement(self.abbreviation_replacement(details))
#             course_detail = row['description']+' '+row['content']
            title = row['courseno'] + ' - ' + row['coursename']
            content[title] = course_detail
        return content
    
    
    def readDictionary(self, base_directory):
        """
            Input   : directory path.
            Returns : Wikipedia article titles and contents ordered list.
        """
        content = {}

        data = json.load(open(base_directory,"r",encoding="utf-8"))
        for title in data:
            temp_title = ''
            temp = title.split('-')
            for i in temp:
                if not re.search('\d+', i):
                    temp_title += i
            details = data[title] + ' ' + temp_title
            details = self.cleanData(details)
            content[title] = self.phrase_replacement(self.abbreviation_replacement(details))
        return content


class ESA:
    def __init__(self, wiki, documents, queries, mode):
        self.wiki = wiki
        self.documents = documents
        self.queries = queries
        self.mode = mode
        
    def dict_to_list(self, dicti):
        titles, contents = [], []
        for key in dicti:
            titles.append(key)
            contents.append(dicti[key])
        return titles, contents
        
    def document_indexing(self, titles):
        content2index = {}
        index2content = {}
        for i in range(len(titles)):
            content2index[titles[i]] = i
            index2content[i] = titles[i]
        return content2index, index2content
    
    def getTFIDFModel(self, documents):
        """
            Input   : list of document contents.
            Returns : TF-IDF Model and TF-IDF Matrix.
        """
        tfidf_vectorizer = TfidfVectorizer(stop_words='english',use_idf=True)
        tfidf_vectorizer.fit(documents)
        document_tfidf_matrix = tfidf_vectorizer.transform(documents)
        vocab = tfidf_vectorizer.vocabulary_
        return document_tfidf_matrix, vocab
    
    def esa_matrix_computation(self, titles, details, vocab, document_matrix):
        num_courses = len(titles)
        esa_matrix = np.zeros((num_courses, self.num_concepts), dtype=float)
        words_not_in_wiki = []
        for i in range(len(titles)):
            i_content = set(details[i].split())
            for word in i_content:
                if word in self.wiki_vocab:
                    word_index_in_documents = vocab[word]
                    word_index_in_wiki    = self.wiki_vocab[word]
                    documents_tf_idf        = document_matrix[word_index_in_documents, i]
                    esa_matrix[i] += documents_tf_idf * self.term_concept_matrix.T[word_index_in_wiki]
                else:
                    words_not_in_wiki.append(word)
        return esa_matrix
    
    def computation(self):
        wiki_titles, wiki_contents = self.dict_to_list(self.wiki)
#         concept2index, index2concept = self.document_indexing(wiki_titles)
        self.term_concept_matrix, self.wiki_vocab = self.getTFIDFModel(wiki_contents)
        self.num_concepts = len(wiki_titles)
        
        document_titles, document_contents = self.dict_to_list(self.documents)
#         document2index, index2document = self.document_indexing(document_titles)
        term_document_matrix, doc_vocab = self.getTFIDFModel(document_contents)
        
        document_esa_matrix = self.esa_matrix_computation(document_titles, document_contents, doc_vocab, term_document_matrix.T)
        
        if self.mode != "same":
            query_titles, query_contents = self.dict_to_list(self.queries)
            query2index, index2query = self.document_indexing(query_titles)
            term_query_matrix, query_vocab = self.getTFIDFModel(query_contents)
            query_esa_matrix = self.esa_matrix_computation(query_titles, query_contents, query_vocab, term_query_matrix.T)
            return document_esa_matrix, query_esa_matrix, cosine_similarity(document_esa_matrix, query_esa_matrix)
        
        return document_esa_matrix, document_esa_matrix, cosine_similarity(document_esa_matrix)

def run_esa():
    SITE_ROOT = os.path.realpath(os.path.dirname("/Users/tapishgarg/Desktop/Course_Overlap/data"))
    json_url = os.path.join(SITE_ROOT, "data", "phrases.json")
    json_data = json.loads(open(json_url).read())
    # print(json_data)
    phrases = json_data
    abbreviations = {}
    with_stemming = 'no'

    # course_detail_path = "../codes/dataset/CourseData.csv"
    course_detail_path = "./data/course_data.json"

    preprocessing = Preprocessing(phrases, abbreviations, with_stemming)
    document_content = preprocessing.readDictionary(course_detail_path)

    wikipedia_articles_path = "./data/wiki_data.json"

    base_content = preprocessing.readDictionary(wikipedia_articles_path)
        
    esa = ESA(base_content, document_content, document_content, "same")
    wiki_document_esa_matrix, wiki_query_esa_matrix, wiki_esa_similarity_matrix = esa.computation()
    print(wiki_esa_similarity_matrix.shape)
    # return np.random.rand(1791,1791)
    return wiki_esa_similarity_matrix