from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from src.infra.schemas import user_schema
from src.infra.database.repositories.user_repository import UserRepository
from src.infra.database.config.database import get_db
from src.core import security
from src.infra.providers import password_provider


router = APIRouter()

@router.post(path='/signup',
            status_code=status.HTTP_201_CREATED,
            response_model=user_schema.UserBase,
            summary='Create a new user',
            )
def signup_user(user: user_schema.UserLogin = Body(...), session: Session = Depends(get_db)):
    # Verify user
    user_reference = UserRepository(session).get_user_by_email(user.email)
    print(user_reference)

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
