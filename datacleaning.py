import re

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.strip()
    # remove URLs
    text = re.sub(r"http\S+|www\.\S+", "", text)
    # remove mentions and hashtags
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    # remove non-alphanumeric (keep spaces)
    text = re.sub(r"[^0-9A-Za-z\s]", "", text)
    # normalize whitespace and lowercase
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text