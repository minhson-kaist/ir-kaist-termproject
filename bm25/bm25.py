import json
import math
import operator
import nltk
import copy
import numpy as np
import jsonlines

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words as nltk_words

from Core import *

porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))
"""
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
"""
word_list = set(nltk.corpus.words.words())


class Preprocess:
    def __init__(self):
        pass

    def lemmatize_tokens(self, tokens, wordnet_lemmatizer):
        '''
        Lemmatization
        :param tokens:
        :param wordnet_lemmatizer:
        :return:
        '''
        lemmatized = []
        for item in tokens:
            lemmatized.append(wordnet_lemmatizer.lemmatize(item))
        return lemmatized

    def stem_tokens(self, tokens, porter_stemmer):
        '''
        Stemming
        :param tokens:
        :param porter_stemmer:
        :return:
        '''
        stemmed = []
        for item in tokens:
            stemmed.append(porter_stemmer.stem(item))
        return stemmed

    def tokenize(self, text):
        '''
        Normalize, lemma, stemming, and stopword
        :param text:
        :return:
        '''
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        lemma = self.lemmatize_tokens(tokens, wordnet_lemmatizer)
        port_stem = self.stem_tokens(lemma, porter_stemmer)
        # Build a list of words ignoring stop worss and illegal characters
        filtered_stems = filter(lambda stem: stem not in stopWords and stem.isalpha() and stem in word_list, port_stem)
        tokens_list = list(copy.deepcopy((filtered_stems)))
        return (tokens_list)


class Dataset:
    def __init__(self, data_path):
        self.data_path = data_path
        self.json_docs = list()
        self.jsl_file = list()
        self.__paragraph_num = 0
        self.token_list = self.getToken()
        self.para_candidates = self.getParaCandidates()

        self.preprocessed = self.preprocess(self.token_list)
        self.vocab_size = len(self.preprocessed)

    def getParaCandidates(self):
        '''
        Get all paragraphs in corpus
        :return:
        '''
        para_candidates = list()
        for i in range (len(self.json_docs)):
            for j in range(len(self.json_docs[i]['long_answer_candidates'])):
                start_token = self.json_docs[i]['long_answer_candidates'][j]['start_token']
                end_token = self.json_docs[i]['long_answer_candidates'][j]['end_token']
                paragraphTokens = self.json_docs[i]['document_tokens'][start_token:end_token]
                para_candidates.append(paragraphTokens)

        return para_candidates


    def setParagraphNum(self, num):
        '''
        Set number of paragraph
        :param num:
        :return:
        '''
        self.__paragraph_num = num

    def getParagraphNum(self):
        '''
        Get number of paragraph
        :return:
        '''
        return self.__paragraph_num

    def displayParagraphNum(self):
        '''
        Display number of paragraph
        :return:
        '''
        print(self.__paragraph_num)

    def getToken(self):
        '''
        Get all tokens in corpus
        :return:
        '''
        token_list = list()
        with jsonlines.open(self.data_path, 'r') as jsl_file:
            self.jsl_file = jsl_file
            for json_dict in jsl_file:
                self.json_docs.append(json_dict)
                token = [json_dict['document_tokens'][x]['token'] for x in range(len(json_dict['document_tokens'])) if(json_dict['document_tokens'][x]['html_token'] == False)]
                token_list += token
                self.__paragraph_num += len(json_dict['long_answer_candidates'])
        return token_list

    def preprocess(self, text):
        '''
        Perform norm, lemma, and stopword here
        :param:
        :return:
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


class RelevanceFeedBack(Dataset):

    def __init__(self):
        Dataset.__init__(self, "nq-dev-sample.jsonl")
        self.core = Core()
        self.query = "" #Query to be filled by user
        self.goal = 0.9
        self.stopWords = set(stopwords.words('english'))

    def RF_Verify(self):
        prepro = Preprocess()
        pass

    def execute(self):
        """
        Execute RF
        """
        print("Please input query")
        self.query = input()
        self.core.query = self.query.split()
        print("Please input target precision")
        try:
            self.goal = float(input())
        except Exception:
            print("Input is not a valid float number, program will exit!")
            return

        print(self)

        totalAns = 10.0
        correctAns = 0.0
        totalLoop = 1

        result_list = "FAke result list here"

        """
        Pick best and worst relevant documents here
        """

        if correctAns / totalAns > self.goal - 1e-6:  # goal achieved, exit program
            print("Precision goal achieved, %d loop(s) used, program will exit." % totalLoop)
            return
        elif correctAns / totalAns < 1e-6:  # precision is 0, exit program
            print("Precision goal is 0, program will exit.")
            return
        else:  # goal not achieved, give information to Core and refine the query
            totalLoop += 1
            correctAns = 0.0
            self.core.input(CoreInputs)
            self.query = self.core.getQuery()
            print("New query is %s, another 10 answer will be shown" % self.query)

class Paragraph:
    def __init__(self, start_token, end_token, json_dict):
        self.json_dict = json_dict
        self.length = 0
        self.paragraph_tokens = {}
        self.start_token = start_token
        self.end_token = end_token
        self.get_paragraph_tokens()

    def get_paragraph_tokens(self):
        '''
        Get token of a paragraph
        :return:
        '''
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
        '''
        Get avg length of paragraphs over a doc
        :return:
        '''
        num_para = len(self.candidates)
        total = 0
        for para in self.candidates:
            total += para.length
        return total/num_para

    #calculats idf according to this formula: https://en.wikipedia.org/wiki/Okapi_BM25
    def get_idf(self, term):
        '''
        Compute idf
        :param term:
        :return:
        '''
        N = len(self.candidates)
        nqi = 0
        for candidate in self.candidates:
            if term in candidate.paragraph_tokens:
                nqi = nqi + 1
        return math.log10((N-nqi+0.5)/(nqi+0.5))

    def bm25(self, paragraph):
        '''
        Compute BM25 for 1 paragraph
        :param paragraph:
        :return:
        '''
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

    def get_candidates(self, json_candidates):
        candidates1 = []
        for c in json_candidates:
            start = c['start_token']
            end = c['end_token']
            candidates1.append(Paragraph(start,end,self.json))
        return candidates1

    #computes bm25 for all the paragraphs
    def bm25_for_all_para(self):
        '''
        Compute BM25 for all paragraphs in a doc with a given query
        :return:
        '''
        score = []
        for candidate in self.candidates:
            score.append((candidate, self.bm25(candidate)))
        return score

class BM25(Dataset):

    def __init__(self):
        Dataset.__init__(self, "nq-dev-sample.jsonl")

    def bm25Score(self):
        bm25_score_list = list()
        for json_dict in self.json_docs:
            d = Document(json_dict)
            score = d.bm25_for_all_para()
            bm25_score = [x[1] for x in score]
            bm25_score_list.append(bm25_score)

        print("The number of document is {}".format(len(bm25_score_list)))
        print("Finish scoring all corpus")

    def bm25Verify(self):
        '''
        Verify BM25 work correctly or not compared to the golden labels
        :return: False/True
        '''

        with jsonlines.open("nq-dev-sample.jsonl", 'r') as jsl_file:
            count = 0
            match = 0
            print(type(jsl_file))
            for json_dict in jsl_file:
                answer_token = list()
                count += 1
                for anno in json_dict['annotations']:
                    start_token = anno['long_answer']['start_token']
                    end_token = anno['long_answer']['end_token']
                    if (start_token == -1 or end_token == -1):
                        continue
                    answer_token.append((start_token, end_token))
                answer_token_set = set(answer_token)
                answer_token_len = len(answer_token_set)

                # print("Answer token len is: {}".format(answer_token_len))
                d = Document(json_dict)
                score = d.bm25_for_all_para()
                bm25_score = [x[1] for x in score]
                index, value = max(enumerate(bm25_score), key=operator.itemgetter(1))
                '''
                print(bm25_score)
                print(index)
                print(value)
                '''
                start_token = score[index][0].start_token
                end_token = score[index][0].end_token
                '''
                print(start_token)
                print(end_token)
                '''
                # count = 0
                hit = False
                for token_set in answer_token_set:
                    if (token_set[0] == start_token and token_set[1] == end_token):
                        hit = True
                        match += 1

        print(count)
        # print(match)

def main():
    run = BM25()
    run.bm25Score()

if __name__ == '__main__':
    main()





