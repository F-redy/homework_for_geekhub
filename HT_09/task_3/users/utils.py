import hashlib
from datetime import datetime


def hash_password(password: str):
    """
    Hash a password using a secure hashing algorithm (e.g., hashlib.sha256).
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def get_create_at():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
