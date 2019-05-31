# document.py

class DocumentQuery:
    """
        Initialize pairs of document and query
    """
    
    def __init__(self, sample):
        self.id = sample['id']
        self.query = sample['query']
        self.query_tokens = sample['query_tokens']
        self.long_answer = sample['long_answer']
        self.long_answer_candidates = sample['long_answer_candidates']
        
    def paragraph_vector(self):
        # generate vectors for paragraph in the list of long_answer_candidates
        list_paragraph_vectors = list()
        
        for paragraph in self.long_answer_candidates:
            sentences = sent_tokenize(paragraph)
            list_sentence_vectors = list()
            paragraph_vector = list()
            #print(paragraph, "\n\n\n")
            for sentence in sentences:
                sentence_tokens = tokenizer.tokenize(sentence)
                #print(sentence_tokens)
                try:
                    indexed_tokens_sentence = tokenizer.convert_tokens_to_ids(sentence_tokens)
                except ValueError:
                    indexed_tokens_sentence = tokenizer.convert_tokens_to_ids(sentence_tokens[:512])

                while len(indexed_tokens_sentence) < 128:
                    indexed_tokens_sentence.append(0)

                sentence_token_tensor = torch.tensor([indexed_tokens_sentence])
                sentence_token_tensor = sentence_token_tensor.to(device)
                sentence_segment_ids = [0]*len(indexed_tokens_sentence)
                sentence_segment_tensors = torch.tensor([sentence_segment_ids])
                sentence_segment_tensors = sentence_segment_tensors.to(device)

                with torch.no_grad():
                    sentence_encoded_layers, _ = model(sentence_segment_tensors, sentence_segment_tensors)
                sentence_vector = sentence_encoded_layers[4][0][1].numpy()
                list_sentence_vectors.append(sentence_vector)
            
            #paragraph_vector = np.average(list_sentence_vectors, axis=0)
            #paragraph_vector.append(list_sentence_vectors)
            list_paragraph_vectors.append(list_sentence_vectors)
        return list_paragraph_vectors
    
    def query_vector(self):
        # return query vector
        query = sample.query
        tokenized_query = tokenizer.tokenize(query)
        indexed_tokens_query = tokenizer.convert_tokens_to_ids(tokenized_query)

        while len(indexed_tokens_query) < 128:
            indexed_tokens_query.append(0)

        tokens_tensor = torch.tensor([indexed_tokens_query])
        tokens_tensor = tokens_tensor.to(device)
        segments_ids = [0] * len(indexed_tokens_query)
        segments_tensors = torch.tensor([segments_ids])
        segments_tensors = segments_tensors.to(device)

        with torch.no_grad():
            encoded_layers, _= model(tokens_tensor, segments_tensors)
        query_vector = encoded_layers[4][0][1]
        return query_vector
    
    def cosine(self):
        # compute cosine similarity for each pair of (query, para)
        # return a list of cosine similarity score
        list_paragraph_vectors = self.paragraph_vector()
        cosine_score_list = list()
        query_vector = self.query_vector().numpy()
        #print(query_vector)
        
        for paragraph_vector in list_paragraph_vectors:
            max_score = 0
            for vector in paragraph_vector:
                #print(vector)
                score = cos_sim(query_vector, vector)
                if score > max_score:
                    max_score = score
            cosine_score_list.append(max_score)
        return cosine_score_list