from src.features.lexical import extract_lexical_features
from src.features.syntactic import extract_syntactic_features
from src.features.stylometrics import extract_stylometric_features
import re
import string
from enum import Enum, auto
import pandas as pd 
import spacy
nlp = spacy.load("en_core_web_sm")

from src.data.gutenberg.book_info import BookInfo
from src.data.utils import chunk_text

from concurrent.futures import ThreadPoolExecutor

class Features(Enum):
    """
    Enum representing types of features that can be extracted from text.
    """
    LEXICAL = auto()
    SYNTACTIC = auto()
    #STYLOMETRICS = auto()
    
def normalize_text(text: str) -> str:
    """
    Normalize input text by lowercasing, removing punctuation and digits,
    and collapsing whitespace.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    text = ' '.join(text.split())
    return text

def extract_features(raw_text: str, features: list[Features] | None = None) -> pd.Series:
    """Extract specified linguistic features from a raw text string."""
    norm_text = normalize_text(raw_text)
    doc = nlp(norm_text)
    extractors = {
        Features.LEXICAL: lambda: extract_lexical_features(norm_text),
        Features.SYNTACTIC:  lambda: extract_syntactic_features(doc),
        #Features.STYLOMETRICS: lambda: extract_stylometric_features(doc)
    }
    result = {}
    for feature in features or list(Features):
        if extractor := extractors.get(feature):
            result |= extractor()
    return pd.Series(result)


def build_feature_dataset(
    books: list[BookInfo],
    features: list | None = None,
    split_text = True,
) -> pd.DataFrame:
    """   
    Build a feature dataset from a list of books by extracting specified features
    optionally splitting texts into chunks for granular feature extraction.
    """
    
    def process_book(book: BookInfo):
        chunks: list[str] = chunk_text(book.text) if split_text else [book.text or ""]
        series_list = []
        for chunk in chunks:
            s = extract_features(chunk, features)
            s["author"] = book.author
            s["title"] = book.title
            series_list.append(s)
        return series_list
    
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_book, books)
    flattened_results = [s for series_list in results for s in series_list]
    return pd.DataFrame(flattened_results)