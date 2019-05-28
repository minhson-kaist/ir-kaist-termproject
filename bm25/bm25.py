import json
import math
import operator

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
def test():
    with open("test.jsonl", 'r') as file:
        for line in file:
            json_dict = json.loads(line)
            d = Document(json_dict)
            score = d.bm25_for_all_para()
            bm25_score = [x[1] for x in score]
            index, value = max(enumerate(bm25_score), key=operator.itemgetter(1))
            print(bm25_score)
            print(index)
            print(value)

def main():
    test()

if __name__ == '__main__':
    main()





