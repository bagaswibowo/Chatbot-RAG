import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'sentence-transformers/all-mpnet-base-v2'

class ChatRetriever:
    def __init__(self, index_path='faiss.index', meta_path='metadata.json', model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)

    def search(self, query, top_k=5):
        query_vec = self.model.encode([query], normalize_embeddings=True)
        D, I = self.index.search(np.array(query_vec, dtype='float32'), top_k)
        results = [self.metadata[i] for i in I[0]]
        return results
