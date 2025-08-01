import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')


def compute_tfidf_features(texts, max_features=1000):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(texts)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=[f"tfidf_{w}" for w in vectorizer.get_feature_names_out()])
    return tfidf_df