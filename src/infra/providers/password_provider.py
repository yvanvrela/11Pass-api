from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt.

    This fuction take a plain password and return the hash password.

    Args:

        password (str): The plain password.

    Returns:

        str: The hased password.
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify Password

    This function verify plain password and hasched password and return a boolean representing match or not.

    Args:

        plain_password (str): Plain password by login.
        hashed_password (str): Hashed password by database.

    Returns:

        bool: True if the password matches hasehd password or False if not match.
    """
    return password_context.verify(plain_password, hashed_password)
