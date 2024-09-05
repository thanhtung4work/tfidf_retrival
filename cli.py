import argparse
import os
import shutil

import numpy
from   PyPDF2 import PdfReader
from   sklearn.feature_extraction.text import TfidfVectorizer
from   sklearn.metrics.pairwise import cosine_similarity

import preprocessing
from   utils import save_uploaded_file, extract_document

# Configure upload folder
UPLOAD_FOLDER = 'documents/'

parser = argparse.ArgumentParser(
    "Document extractor",
    description="CLI application for managing, extracting, retrieving documents"
)

parser.add_argument("--retrieve", type=bool, help="Retrieve query")
parser.add_argument("--add-document", type=str, help="Add document to storage")


def retrieve():
    while True:
        q = input("what's your query? (type quit to stop) ")
        if q == "quit": break
        sim_index = extract_document(
            q,
            UPLOAD_FOLDER
        )
        print(sim_index)

def add_document(filename: str):
    shutil.copyfile(filename, f"documents/{os.path.basename(filename)}")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.add_document:
        add_document(args.add_document)
    
    if args.retrieve:
        retrieve()