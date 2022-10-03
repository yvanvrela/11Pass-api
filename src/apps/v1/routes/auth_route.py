from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from src.infra.schemas import user_schema
from src.infra.database.repositories import user_repository
from src.infra.database.config.database import get_db


router = APIRouter()


@router.get(path='/signup/',
            #  status_code=status.HTTP_201_CREATED,
            #  response_model=user_schema.UserBase,
            #  summary='Create a new user',
            )
def signup_user(
    # user: user_schema.UserLogin = Body(...),
                # session: Session = Depends(get_db)
                ):
    return {'hello': 'world'}
