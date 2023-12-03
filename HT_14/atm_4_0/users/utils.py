import hashlib


def hash_password(password: str):
    """ Хеширует пароль, используя безопасный алгоритм хеширования. (hashlib.sha256). """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password
