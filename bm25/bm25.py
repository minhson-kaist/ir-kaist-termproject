import json
import math
import operator
import nltk
import copy
import numpy as np

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words as nltk_words

porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

word_list = set(nltk.corpus.words.words())

def tokenize(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    lemma = lemmatize_tokens(tokens, wordnet_lemmatizer)
    port_stem = stem_tokens(lemma, porter_stemmer)
	# Build a list of words ignoring stop worss and illegal characters
    filtered_stems = filter(lambda stem: stem not in stop_words and stem.isalpha() and stem in word_list, port_stem)
    return filtered_stems

class Dataset:
    def __init__(self, data_path):
        self.data_path = data_path
        self.paragraph_num = 0
        self.token_list = self.getToken()
        print(len(self.token_list))
        print(type(self.token_list[100]))
        self.preprocessed = self.preprocess(self.token_list)
        self.vocab_size = len(self.preprocessed)
        print(len(self.preprocessed))
        print(self.paragraph_num)

    def getToken(self):
        token_list = list()
        with open(self.data_path, 'r') as file:
            for line in file:
                json_dict = json.loads(line)
                token = [json_dict['document_tokens'][x]['token'] for x in range(len(json_dict['document_tokens'])) if(json_dict['document_tokens'][x]['html_token'] == False)]
                token_list += token
                self.paragraph_num += len(json_dict['long_answer_candidates'])
                #print(len(token_list))
                #print("con meo")
        return token_list

    def buildVector(self):
        words_matrix = np.zeros((self.paragraph_num, self.vocab_size))
        # build vector representation for paragraph
        tmp_vec = np.zeros(self.vocab_size)
        for i in range(len(self.paragraph_num)):
            pass

    def preprocess(self, text):
        '''
        Preprocess raw text to get tokens
        :param: text: Input text (string)
        :return: vocab_entries: Output vocabulary (filter)
        '''

        stemmed = []
        lemmatized = []
        wordsFiltered = []

        # Normalization
        norm_text = [text[x].lower() for x in range(len(text))]

        # Tokenization
        token_text = text

        # Lemmatization
        for token in token_text:
            lemmatized.append(wordnet_lemmatizer.lemmatize(token))

        wordsFiltered = filter(lambda
                                   word_to_filter: word_to_filter not in stopWords and word_to_filter.isalpha() and word_to_filter in word_list,
                               lemmatized)

        vocab_entries = wordsFiltered

        tokens_list = list(copy.deepcopy((vocab_entries)))
        return tokens_list

class Paragraph:
    def __init__(self, start_token, end_token, json_dict):
        self.json_dict = json_dict
        self.length = 0
        self.paragraph_tokens = {}
        self.start_token = start_token
        self.end_token = end_token
        self.get_paragraph_tokens()

    def get_paragraph_tokens(self):
        current_tokens = self.json_dict['document_tokens'][self.start_token:self.end_token]

        for elem in current_tokens:
            if not elem["html_token"]:
                self.length += 1
                self.paragraph_tokens[elem["token"]] = self.paragraph_tokens.get(elem["token"], 0) + 1

class Document:

    def __init__ (self, json1):
        self.json = json1
        self.id = json1["example_id"]
        self.query = json1["question_tokens"]
        self.candidates = self.get_candidates(json1["long_answer_candidates"])
        self.avgdl = self.get_avgdl()

    #gets the average paragraph length
    def get_avgdl(self):
        num_para = len(self.candidates)
        total = 0
        for para in self.candidates:
            total += para.length
        return total/num_para

    #calculats idf according to this formula: https://en.wikipedia.org/wiki/Okapi_BM25
    def get_idf(self, term):
        N = len(self.candidates)
        nqi = 0
        for candidate in self.candidates:
            if term in candidate.paragraph_tokens:
                nqi = nqi + 1
        return math.log10((N-nqi+0.5)/(nqi+0.5))

    #computse bm25 for 1 paragraph
    def bm25(self, paragraph):
        score = 0
        k1 = 1.2
        b = 0.75

        for q in self.query:
            if q in paragraph.paragraph_tokens:
                tf = paragraph.paragraph_tokens[q]
            else:
                tf = 1

            dl = paragraph.length
            score += (self.get_idf(q)*tf*(k1+1))/(tf + k1*(1-b+b*(dl/self.avgdl)))
        return score

    #creates all the paragraphs and returns a list of em
    def get_candidates(self, json_candidates):
        candidates1 = []
        for c in json_candidates:
            start = c['start_token']
            end = c['end_token']
            candidates1.append(Paragraph(start,end,self.json))
        return candidates1

    #computes bm25 for all the paragraphs
    def bm25_for_all_para(self):
        score = []
        for candidate in self.candidates:
            score.append((candidate, self.bm25(candidate)))
        return score
def _verify():
    with open("test.jsonl", 'r') as file:
        for line in file:
            json_dict = json.loads(line)
            answer_token = list()
            for anno in json_dict['annotations']:
                start_token = anno['long_answer']['start_token']
                end_token = anno['long_answer']['end_token']
                if (start_token == -1 or end_token == -1):
                    continue
                answer_token.append((start_token, end_token))
            answer_token_set = set(answer_token)
            answer_token_len = len(answer_token_set)

            #print("Answer token len is: {}".format(answer_token_len))
            d = Document(json_dict)
            score = d.bm25_for_all_para()
            bm25_score = [x[1] for x in score]
            index, value = max(enumerate(bm25_score), key=operator.itemgetter(1))
            print(bm25_score)
            print(index)
            print(value)
            start_token = score[index][0].start_token
            end_token = score[index][0].end_token

            print(start_token)
            print(end_token)

            match = False
            for token_set in answer_token_set:
                if(token_set[0] == start_token and token_set[1] == end_token):
                    match = True

            print(match)

def _rel_feedback():
    a = Dataset("test.jsonl")

def main():
    #_verify()
    _rel_feedback()

if __name__ == '__main__':
    main()





