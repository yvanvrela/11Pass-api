from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# Database
from sqlalchemy.orm import Session
from src.infra.database.config.database import get_db
from src.infra.providers import password_provider
# Repository
from src.infra.database.repositories.user_repository import UserRepository
# JWT
from jose import JWTError
from src.infra.providers import token_provider
# Model
from src.infra.database.models.user_model import UserModel
# Settings
from src.core.settings import Settings


settings = Settings()
url_prefix = settings.api_prefix_router

# Instance the login url and to validate token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{url_prefix}/auth/login')


def authenticate_user(user_email: str, password: str, session: Session = Depends(get_db)) -> UserModel | bool:
    """Authenticate user

    This is function recibed the username and password and verify to exists and the password is correct.

    Args:

        user_email (str): This is the user email.
        password (str): This is the user password.

    Returns:

        UserModel | bool: UserModel is the user object or bool default is False.
    """
    user = UserRepository(session).get_user(user_email)
    if not user:
        return False
    if not password_provider.verify_password(password, user.password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> UserModel:
    """Get current user

    This is function recibed a token and verify the token is correct.

    Args:

        token (str): This is the user token. Defaults to Depends(oauth2_scheme).

    Raises:

        credentials_exception: code:401, detail:Could not validate credentials, headers:{WWW-Authenticate: Bearer} 

    Returns:
        UserModel: UserModel is the user object
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        email = token_provider.verify_token(token)
    except JWTError:
        raise credentials_exception

    user = UserRepository(session).get_user(email)
    if user is None:
        raise credentials_exception
    return user
