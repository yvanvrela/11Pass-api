from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
# Settings
from src.core.settings import Settings

settings = Settings()

# Conts of jwt
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm_type
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire


def create_access_token(data: dict, expieres_delta: timedelta | None = None) -> str:
    """Create access token

    This is function recibed the user information and expire time of save in the token. 

    Args:

        data (dict): This is the user information to encode.
        expieres_delta (timedelta | optional): This the expire time. Defaults to None.

    Returns:

        str: str is the user token.
    """

    to_encode = data.copy()

    if expieres_delta:
        expire = datetime.utcnow() + expieres_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=10)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_token(token: str):
    to_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return to_decode.get('sub')
