import regex as re
import unicodedata

def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
