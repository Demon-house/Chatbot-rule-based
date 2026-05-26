import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import difflib

class Chatbot:
    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open("dataset.json", "r") as f:
            self.data = json.load(f)

        self.questions = [d["question"] for d in self.data]
        self.answers = [d["answer"] for d in self.data]

        self.embeddings = self.model.encode(self.questions)

        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings).astype("float32"))

        self.words = [
            "numpy","pandas","matplotlib","seaborn","tensorflow",
            "pytorch","scikit-learn","flask","html","css","javascript"
        ]

    def fix(self, text):
        words = text.lower().split()
        out = []

        for w in words:
            match = difflib.get_close_matches(w, self.words, n=1, cutoff=0.7)
            out.append(match[0] if match else w)

        return " ".join(out)

    def get_response(self, query):

        query = self.fix(query)

        vec = self.model.encode([query])

        D, I = self.index.search(np.array(vec).astype("float32"), 1)

        idx = I[0][0]
        dist = D[0][0]

        if dist > 1.2:
            return "Sorry, I don't know this topic."

        return self.answers[idx]