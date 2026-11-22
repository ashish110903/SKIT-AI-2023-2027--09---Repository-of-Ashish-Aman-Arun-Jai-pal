import hashlib
def compute_data_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f: h.update(f.read())
    return h.hexdigest()
