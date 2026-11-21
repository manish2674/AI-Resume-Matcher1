
import re
import unicodedata


def normalize_unicode(text: str) -> str:
    """Normalize Unicode characters consistently."""

    return unicodedata.normalize("NFKC", text)


def remove_unwanted_characters(text: str) -> str:
    """Remove control characters while preserving useful punctuation."""

    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", " ", text)

    return text


def normalize_whitespace(text: str) -> str:
    """Normalize spaces and blank lines."""

    # Replace tabs and repeated spaces with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    # Limit excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_text(text: str) -> str:
    """Apply all text-cleaning operations."""

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text = normalize_unicode(text)
    text = remove_unwanted_characters(text)
    text = normalize_whitespace(text)

    return text
