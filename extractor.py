import os

import numpy
from   PyPDF2 import PdfReader
from   sklearn.feature_extraction.text import TfidfVectorizer
from   sklearn.metrics.pairwise import cosine_similarity

import preprocessing

documents = []
files = os.listdir("documents")
for filename in files:
    reader = PdfReader(f"documents/{filename}")

    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    text = preprocessing.to_lower(text)
    text = preprocessing.remove_punc(text)
    text = preprocessing.remove_whitespace(text)
    documents.append(text)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)
numpy.save("retrival_matrix/retrival_matrix.npy", tfidf_matrix)

while True:
    q = input("what's your query? ")
    if q == "quit": break
    query = [q]
    query_vec = vectorizer.transform(query)
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    for file, score in zip(files, similarities):
        print(f"{file:<{24}}: {score}")