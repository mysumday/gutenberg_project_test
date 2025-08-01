import spacy
from collections import Counter
from spacy.tokens import Doc

nlp = spacy.load("en_core_web_sm")

def extract_syntactic_features(doc: Doc):
    """
    Extract syntactic features from a spaCy Doc object.

    Features extracted:
    - Average sentence length (in words)
    - Ratio of sentences written in passive voice
    - Relative frequency of each part-of-speech (POS) tag in the document
    """
    
    pos_tags = [token.pos_ for token in doc if not token.is_punct]
    total_tokens = len(pos_tags)
    pos_freq = Counter(pos_tags)
    pos_features = {f"pos_{tag}": count / total_tokens for tag, count in pos_freq.items()}
    
    # TODO: N grams logic
    # pos_ngrams = [' '.join(pos_tags[i:i+n]) for i in range(len(pos_tags) - n + 1)]
    # pos_ngram_freq = Counter(pos_ngrams)
    # top_pos_ngrams = dict(pos_ngram_freq.most_common(10))
    # top_pos_ngrams = {f"pos_ngram_{ng}": freq / total_tokens for ng, freq in top_pos_ngrams.items()}
    
    sentence_lengths = [len(sent) for sent in doc.sents]
    avg_sent_len = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

    passive_sentences = 0
    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "auxpass":
                passive_sentences += 1
                break
    passive_ratio = passive_sentences / len(list(doc.sents)) if doc.sents else 0
    return {
        "avg_sentence_length_words": avg_sent_len,
        "passive_voice_ratio": passive_ratio,
        **pos_features,
    }