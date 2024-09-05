import os

import numpy
from   PyPDF2 import PdfReader
from   sklearn.feature_extraction.text import TfidfVectorizer
from   sklearn.metrics.pairwise import cosine_similarity

import preprocessing


def save_uploaded_file(file, upload_folder):
    """
    Function to save uploaded file
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path


def extract_document(query, document_storage="documents"):
    documents = []
    # Read documents in storage
    files = os.listdir(document_storage)
    for filename in files:
        reader = PdfReader(f"{document_storage}/{filename}")

        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        text = preprocessing.to_lower(text)
        text = preprocessing.remove_punc(text)
        text = preprocessing.remove_whitespace(text)
        documents.append(text)

    # Create bag of word
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Create word vector
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    sim_index = {}
    for file, score in zip(files, similarities):
        sim_index[file] = score
    return sim_index