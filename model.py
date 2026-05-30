import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib


class Chatbot:

    def __init__(self):

       
        with open("dataset.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.questions = [x["question"] for x in self.data]
        self.answers = [x["answer"] for x in self.data]

        
        self.vectorizer = TfidfVectorizer()
       
        self.q_vectors = self.vectorizer.fit_transform(self.questions)

       
        self.words = [
            "numpy",
            "tensorflow",
            "pandas",
            "pytorch",
            "flask",
            "html",
            "css",
            "javascript"
        ]

    def fix(self, text):

        words = text.lower().split()

        out = []

        for w in words:

            match = difflib.get_close_matches(
                w,
                self.words,
                n=1,
                cutoff=0.7
            )

            out.append(match[0] if match else w)

        return " ".join(out)

    def get_response(self, query):

        query = self.fix(query)

        
        vec = self.vectorizer.transform([query])

       
        sims = cosine_similarity(vec, self.q_vectors)[0]

        idx = int(np.argmax(sims))

        score = float(sims[idx])

       
        if score < 0.2:
            return "Sorry, I don't know this topic."

        return self.answers[idx]