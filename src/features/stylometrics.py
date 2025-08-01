import os
import spacy
import textstat
import pandas as pd
from spacy.tokens import Doc
from typing import Any


def extract_stylometric_features(doc: Doc) -> dict[str, Any]:
    """
    Extract stylometric readability and structural features from a spaCy Doc object.

    This function computes various readability scores and text structure metrics including:
    - Flesch Reading Ease score,
    - Flesch-Kincaid Grade Level,
    - Automated Readability Index (ARI),
    - Average sentence length (in tokens, excluding punctuation),
    - Average paragraph length (in sentences),
    - Ratio of long words (length > 6),
    - Ratio of short words (length ≤ 3).
    """
    
    flesch_reading_ease = textstat.flesch_reading_ease(doc.text) # pyright: ignore[reportAttributeAccessIssue]
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(doc.text) # pyright: ignore[reportAttributeAccessIssue]
    ari_score = textstat.automated_readability_index(doc.text) # pyright: ignore[reportAttributeAccessIssue]
    
    sentences = list(doc.sents)
    sentence_lengths = [
        len([
            token for token in sent
            if not token.is_punct
        ]) 
        for sent in sentences
    ]
    avg_sentence_len = sum(sentence_lengths) / len(sentences) if sentences else 0
    
    paragraphs = [p for p in doc.text.split('\n') if p.strip()]
    sents = list(doc.sents)
    paragraph_boundaries = [(doc.text.find(p), doc.text.find(p) + len(p)) for p in paragraphs]

    paragraph_lengths = [
        sum(
            start >= p_start and start < p_end 
            for sent in sents 
            for start in [sent.start_char]
            )
        for p_start, p_end in paragraph_boundaries
    ]    
    
    words = [t.text for t in doc if t.is_alpha]
    long_words = [w for w in words if len(w) > 6]
    short_words = [w for w in words if len(w) <= 3]
    long_word_ratio = len(long_words) / len(words) if words else 0
    short_word_ratio = len(short_words) / len(words) if words else 0

    return {
        "flesch_reading_ease": flesch_reading_ease,
        "flesch_kincaid_grade": flesch_kincaid_grade,
        "automated_readability_index": ari_score,
        "avg_sentence_length": avg_sentence_len,
        "avg_paragraph_length": paragraph_lengths,
        "long_word_ratio": long_word_ratio,
        "short_word_ratio": short_word_ratio,
    }