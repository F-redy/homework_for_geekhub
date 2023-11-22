import hashlib


def hash_password(password: str):
    """ Hash a password using a secure hashing algorithm (e.g., hashlib.sha256). """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password
