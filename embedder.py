from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

MODEL_NAME = 'sentence-transformers/all-mpnet-base-v2'

class ChatEmbedder:
    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.metadata = []

    def embed_chats(self, chats, progress_callback=None):
        texts = [f"[{c['timestamp']}] {c['sender']}: {c['message']}" for c in chats]
        total = len(texts)
        embeddings = []
        batch_size = 32
        for i in range(0, total, batch_size):
            batch = texts[i:i+batch_size]
            emb = self.model.encode(batch, normalize_embeddings=True)
            embeddings.append(emb)
            if progress_callback:
                percent = int((i+len(batch))/total*100)
                progress_callback(percent)
        embeddings = np.vstack(embeddings)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(np.array(embeddings, dtype='float32'))
        self.metadata = chats

    def save(self, index_path='faiss.index', meta_path='metadata.json'):
        faiss.write_index(self.index, index_path)
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def load(self, index_path='faiss.index', meta_path='metadata.json'):
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
