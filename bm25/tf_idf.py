import json

num_docs = 0
term_freq = {}

doc_term_freq = {}
'''
builds a dictionary(term_freq) with the DF for each term in the documents
term_freq["hello"] = total number of times hello appears in all document in the file test.jsonl 
'''
class Document:

    def __init__ (self, json):
        self.json = json
        self.id = json["example_id"]
        self.query = json["question_tokens"]
        self.doc_tokens = json["document_tokens"]
        self.candidates = self.get_candidates(json["long_answer_candidates"])




    def get_candidates(self, json_candidates):
        candidates = {}
        for c in json_candidates:
            #for t in self.doc_tokens:
            start = c['start_token']
            end = c['end_token']

            current = self.doc_tokens[start:end]
            current_ans= []
            for elem in current:
                if not elem["html_token"]:
                    current_ans.append(elem["token"])
            candidates[start, end] = current_ans


        print(candidates)



with open("test.jsonl", 'r') as file:
    for line in file:
        json_dict = json.loads(line)
        d = Document(json_dict)
       # print(d.candidates)

"""
class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.query = dict() #query[example_id] = question tokens
        self.document = dict() #document[example_id][hello] = number of times hello appears in example id
        self.token_start_byte = dict()
        self.documentTokens = dict()
        self.candidates = dict()

    def parse(self):
        with open(self.filename, 'r') as file:
            for line in file:
                json_dict = json.loads(line)
                docid = json_dict["example_id"]
                self.query[docid] = json_dict["question_tokens"]
                self.candidates[docid] = json_dict["long_answer_candidates"]
                # self.document[docid] = json_dict["document_tokens"]#[0]["token"]
                self.document[docid] = {}
                self.token_start_byte[docid] = {}
                self.documentTokens[docid] = json_dict["document_tokens"]


                for elem in json_dict["document_tokens"]:
                    self.token_start_byte[docid][elem["start_byte"]] = elem["token"]
                    if elem["html_token"] == False:
                       self.document[docid][elem["token"]] = self.document[docid].get(elem["token"], 0) + 1
        print(self.token_start_byte)
    
        def get_candidates(self):
        for document in self.candidates:
            for candidate in document:
                start_byte = candidate["start_byte"] 
                end_byte = candidate["end_byte"]
    


p = Parser("test.jsonl")
p.parse()



        def doc_frequency(self):
        global term_freq
        global num_docs
        global doc_term_freq
        with open('test.jsonl', 'r') as file:
            for line in file:
                num_docs += 1
                json_dict = json.loads(line)
                docid = json_dict["example_id"]
                doc_term_freq[docid] = {}
                for token in json_dict["document_tokens"]:
                    if str(token["token"]).isalnum() and token["html_token"] != True:
                        key = str(token["token"].lower())
                        term_freq[key] = term_freq.get(key, 0) + 1
                        doc_term_freq[docid][key] = doc_term_freq[docid].get(key, 0) + 1

    def term_frequency(documentid, term):
        print(doc_term_freq)


    doc_frequency()
    term_frequency(1, "high")
    #term_frequency("hejdåhej", "hej")


"""
