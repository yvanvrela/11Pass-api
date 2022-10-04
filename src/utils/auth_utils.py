from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# Database
from sqlalchemy.orm import Session
from src.infra.database.config.database import get_db
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

    user = UserRepository(session).get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user
