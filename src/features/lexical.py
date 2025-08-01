import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import Any

nltk.download('punkt')
nltk.download('stopwords')
function_words = set(stopwords.words('english'))

def extract_lexical_features(normalized_text: str) -> dict[str, Any]:
    """
    Extract lexical features from a normalized text string.

    This function tokenizes the input text and calculates various lexical statistics:
    - total number of words,
    - number of unique words,
    - type-token ratio (unique words / total words),
    - average word length,
    - hapax legomena ratio (words occurring once / total words),
    - relative frequencies of predefined function words.
    """
    tokens: list[str] = word_tokenize(normalized_text)
    clean_tokens = [token for token in tokens if token.isalpha()]

    total_words = len(tokens)
    unique_words = set(tokens)
    word_counts = Counter(tokens)
    
    token_ratio = len(unique_words) / total_words if total_words else 0
    function_word_counts = {fw: tokens.count(fw) / total_words for fw in function_words}
    avg_word_len = sum(len(word) for word in tokens) / total_words if total_words else 0
    hapax_legomena = len([w for w in word_counts if word_counts[w] == 1])
    hapax_ratio = hapax_legomena / total_words if total_words else 0
    

    return {
        'total_words': total_words,
        'unique_words': len(unique_words),
        'type_token_ratio': token_ratio,
        'avg_word_length': avg_word_len,
        'hapax_ratio': hapax_ratio,
        **function_word_counts
    }