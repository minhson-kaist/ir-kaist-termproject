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
        
    def BM25(self):
        """
        Compute BM25 score of query and each paragraph in the document.
        Return list of dictionaries, each dictionary contains paragraph id and its BM25 score
        """
        
        return
    