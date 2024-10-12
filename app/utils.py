from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def Hash(Str: str) -> str:
    """ Hash the given string """
    return bcrypt_context.hash(Str)
