from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hash, password) -> bool:
    return ph.verify(hash, password)


def needs_rehash(hash) -> bool:
    return ph.check_needs_rehash(hash)
