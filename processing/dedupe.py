import hashlib

def hash_row(text, username):
    return hashlib.sha256((text + username).encode("utf-8")).hexdigest()
