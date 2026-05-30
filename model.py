import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib


class Chatbot:

    def __init__(self):

        # Use a local TF-IDF vectorizer instead of a remote pre-trained model
        with open("dataset.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.questions = [x["question"] for x in self.data]
        self.answers = [x["answer"] for x in self.data]

        # Build TF-IDF matrix for all questions (local, no external downloads)
        self.vectorizer = TfidfVectorizer()
        # q_vectors is a (n_questions x n_features) sparse matrix
        self.q_vectors = self.vectorizer.fit_transform(self.questions)

        # small vocabulary used for fuzzy corrections
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

        # vectorize query using local TF-IDF
        vec = self.vectorizer.transform([query])

        # cosine similarity between query and all questions
        sims = cosine_similarity(vec, self.q_vectors)[0]

        idx = int(np.argmax(sims))

        score = float(sims[idx])

        # threshold for unknown topics (tweakable)
        if score < 0.2:
            return "Sorry, I don't know this topic."

        return self.answers[idx]