import json
import random

topics = [
    ("What is Python", "Python is a high-level programming language used for AI, web development, and data science."),
    ("What is Flask", "Flask is a lightweight Python web framework used to build web apps."),
    ("What is Django", "Django is a full-stack Python web framework."),
    ("What is AI", "AI stands for Artificial Intelligence."),
    ("What is Machine Learning", "Machine Learning allows systems to learn from data."),
    ("What is Deep Learning", "Deep Learning is a subset of Machine Learning."),
    ("What is NumPy", "NumPy is used for numerical computing."),
    ("What is Pandas", "Pandas is used for data analysis."),
    ("What is TensorFlow", "TensorFlow is a deep learning framework."),
    ("What is PyTorch", "PyTorch is a deep learning framework."),
    ("What is HTML", "HTML is used to structure web pages."),
    ("What is CSS", "CSS is used to style web pages."),
    ("What is JavaScript", "JavaScript makes web pages interactive."),
    ("What is SQL", "SQL is used to manage databases."),
    ("What is Git", "Git is a version control system."),
    ("What is GitHub", "GitHub is a code hosting platform."),
    ("What is API", "API allows communication between software systems."),
    ("How to install Python", "Download Python from python.org and install it."),
    ("How to install Flask", "Run pip install flask"),
    ("How to install NumPy", "Run pip install numpy"),
    ("How to install Pandas", "Run pip install pandas"),
    ("How to install TensorFlow", "Run pip install tensorflow"),
    ("How to install PyTorch", "Run pip install torch torchvision"),
    ("How to install AI libraries", "Use pip install numpy pandas scikit-learn tensorflow"),
]

patterns = [
    "What is {}",
    "Explain {}",
    "Tell me about {}",
    "Define {}",
    "Give information about {}",
    "What do you mean by {}",
    "Describe {}",
    "Why use {}",
    "{} meaning",
    "Use of {}"
]

dataset = []

while len(dataset) < 1000:

    topic, answer = random.choice(topics)
    pattern = random.choice(patterns)

    question = pattern.format(topic.lower())

    dataset.append({
        "question": question,
        "answer": answer
    })

with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4)

print("Dataset created with", len(dataset), "entries")