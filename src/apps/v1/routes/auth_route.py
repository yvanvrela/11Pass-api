from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from src.infra.schemas import user_schema, token_schema
from src.infra.database.repositories.user_repository import UserRepository
from src.infra.database.config.database import get_db
from src.core import security
from src.infra.providers import password_provider, token_provider
from src.utils import auth_utils


router = APIRouter()


@router.post(path='/signup',
             status_code=status.HTTP_201_CREATED,
             response_model=user_schema.UserBase,
             summary='Create a new user',
             )
def signup_user(user: user_schema.UserLogin = Body(...), session: Session = Depends(get_db)):
    # Verify user
    user_reference = UserRepository(session).get_user(user.email)

    if user_reference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered.'
        )

    # Generate the user secret key
    user.secret_key = security.secret_key_generator()

    # Create new user
    user.password = password_provider.hash_password(user.password)
    user_db = UserRepository(session).create_user(user)

    return user_db


@router.post(path='/login',
             status_code=status.HTTP_200_OK,
             response_model=token_schema.Token,
             summary='Login a user'
             )
def login_for_access_token(login_data: user_schema.UserLoginForm, session: Session = Depends(get_db)):

    user_reference = auth_utils.authenticate_user(
        login_data.email, login_data.password, session)

    if not user_reference:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Token Generate
    accesss_token = token_provider.create_access_token(
        {'sub': user_reference.email})

    return token_schema.Token(access_token=accesss_token, token_type='bearer')
