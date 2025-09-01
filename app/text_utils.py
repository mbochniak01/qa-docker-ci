import re


def clean_text(text: str) -> str:
    """
    Clean input text:
    - Lowercase
    - Remove punctuation
    - Remove extra spaces
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # normalize spaces
    return text
