from fastapi import APIRouter, Depends, Body, Path, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from src.core import security
from src.infra.schemas import account_schema
from src.infra.database.models import user_model, vault_model, account_model
from src.infra.database.repositories.account_repository import AccountRepository
from src.infra.database.config.database import get_db
from src.utils.auth_utils import get_current_user


router = APIRouter()


@router.post(path='/',
             status_code=status.HTTP_201_CREATED,
             response_model=account_schema.AccountOut,
             summary='Create a account.'
             )
def create_account(
    account: account_schema.AccountBase,
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    # Verify user
    if current_user.id != account.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.',
        )

    # Verify account name reference
    account_name_reference = AccountRepository(session).get_account_by_name(
        account_name=account.name, user_id=current_user.id)
    if account_name_reference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Account name already exists.'
        )

    secret_key = security.decode_secret_key(secret_key_encode=current_user.secret_key, current_user=current_user)
    # Encrypt password
    account.password = security.encode_password(password=account.password, secret_key=secret_key)

    # Add to db
    account_db = AccountRepository(session).create_account(account)

    return account_db
