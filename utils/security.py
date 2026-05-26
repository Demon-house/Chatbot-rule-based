import re

def clean_input(text):
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^\w\s,?!.]", "", text)
    return text.strip()