import argparse
import os
import shutil

import numpy
from   PyPDF2 import PdfReader
from   sklearn.feature_extraction.text import TfidfVectorizer
from   sklearn.metrics.pairwise import cosine_similarity

import preprocessing

parser = argparse.ArgumentParser(
    "Document extractor",
    description="CLI application for managing, extracting, retrieving documents"
)

parser.add_argument("--retrieve", type=bool, help="Retrieve query")
parser.add_argument("--add-document", type=str, help="Add document to storage")


def retrieve():
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
        q = input("what's your query? (type quit to stop) ")
        if q == "quit": break
        query = [q]
        query_vec = vectorizer.transform(query)
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        for file, score in zip(files, similarities):
            print(f"{file:<{24}}: {score}")

def add_document(filename: str):
    shutil.copyfile(filename, f"documents/{os.path.basename(filename)}")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.add_document:
        add_document(args.add_document)
    
    if args.retrieve:
        retrieve()