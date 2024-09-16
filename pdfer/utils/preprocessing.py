import re
import string

def to_lower(text: str):
    return text.lower()

def remove_punc(text: str):
    return text.translate(str.maketrans("", "", string.punctuation))

def remove_whitespace(text: str):
    text = text.strip()
    text = " ".join(text.split())
    return text

def remove_nums(text: str):
    return re.sub(r"\d+", "", text)