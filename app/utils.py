"""Utility functions"""
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def Hash(Str: str) -> str:
    """ Hash the given string
     Args:
         Str: string to hash
    Returns:
        (str): hashed string
    """
    return bcrypt_context.hash(Str)


def verifiy_hash(Str: str, Hash: str) -> bool:
    """ Verify the hash
     Args:
         Str: verify string
         Hash: existing hash
    Returns:
        (bool): True if hashed string is source string
    """
    return bcrypt_context.verify(Str, Hash)
