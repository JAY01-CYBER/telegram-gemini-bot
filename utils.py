import re

def clean_text(text: str) -> str:
    """
    Clean input text by:
    - Stripping leading/trailing whitespace
    - Removing extra spaces
    - Normalizing multiple newlines
    """
    if not isinstance(text, str):
        return ""

    # Trim whitespace
    text = text.strip()

    # Replace multiple spaces with single space
    text = re.sub(r"\s+", " ", text)

    # Normalize multiple newlines
    text = re.sub(r"\n+", "\n", text)

    return text
