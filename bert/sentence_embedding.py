# sentence_embedding.py

import logging
import matplotlib.pyplot as plt 
import torch
from pytorch_pretrained_bert import BertModel, BertTokenizer
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import numpy as np
from numpy import dot
from numpy.linalg import norm
logger = logging.getLogger(__name__)

# compute cosine similarity
def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))

# load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# load BERT model to device
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()
model.to(device)