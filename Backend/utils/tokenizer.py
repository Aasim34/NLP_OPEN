"""
Tokenizer utility module.
Handles text normalization and splitting input sentences into
individual word tokens using NLTK.
"""

import re

import nltk

# Download the punkt tokenizer data (only needed once)
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)


def normalize(text: str) -> str:
    """
    Normalize the input text before tokenization.

    Steps:
        - Convert to lowercase.
        - Collapse multiple spaces into one.
        - Strip leading / trailing whitespace.

    Args:
        text: Raw input string.

    Returns:
        Cleaned text string.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(sentence: str) -> list[str]:
    """
    Normalize and tokenize the input sentence into a list of words.

    Args:
        sentence: The input text to tokenize.

    Returns:
        A list of word tokens.
    """
    sentence = normalize(sentence)
    tokens = nltk.word_tokenize(sentence)
    return tokens
