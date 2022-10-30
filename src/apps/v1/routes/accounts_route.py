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
    account: account_schema.AccountCreate,
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

    secret_key = security.decode_secret_key(
        secret_key_encode=current_user.secret_key)
    # Encode password
    account.password = security.encode_password(
        password=account.password, secret_key=secret_key)

    # Add to db
    account_db = AccountRepository(session).create_account(account)

    return account_db


@router.get(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=account_schema.AccountCreate,
            summary='Get account by id',
            )
def get_account(
    id: int = Path(..., gt=0, example=1),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    account_db = AccountRepository(session).get_account_by_id(
        account_id=id, user_id=current_user.id)
    if not account_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Account not found.',
        )

    decode_password = security.decode_password(
        password_encode=account_db.password,
        secret_key=security.decode_secret_key(
            secret_key_encode=current_user.secret_key
        )
    )

    account_db.password = decode_password

    return account_db


@router.get(path='/',
            status_code=status.HTTP_200_OK,
            response_model=List[account_schema.AccountOut],
            summary='Get all user accounts.',
            )
def get_accounts(
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    accounts_db = AccountRepository(
        session).get_accounts(user_id=current_user.id)
    if not accounts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Accounts not found.',
        )

    # Decode all passwords
    for account in accounts_db:
        decode_password = security.decode_password(
            password_encode=account.password,
            secret_key=security.decode_secret_key(
                secret_key_encode=current_user.secret_key
            )
        )
        account.password = decode_password

    return accounts_db


@router.put(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=account_schema.AccountOut,
            summary='Update a account',
            )
def update_account(
    id: int = Path(..., gt=0, example=1,),
    update_data: account_schema.AccountCreate = Body(...,),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    # Verify account
    account_reference = AccountRepository(session).get_account_by_id(
        account_id=id, user_id=current_user.id)
    if not account_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Account not found.'
        )

    # Verify account name duplicate in db
    new_name = update_data.name
    old_name = account_reference.name
    if new_name != old_name:
        account_name_reference = AccountRepository(session).get_account_by_name(
            account_name=new_name, user_id=current_user.id)
        if account_name_reference:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Account name already exists.'
            )

    secret_key = security.decode_secret_key(
        secret_key_encode=current_user.secret_key)

    # Encode password
    update_data.password = security.encode_password(
        password=update_data.password, secret_key=secret_key)

    # Add to db
    account_db = AccountRepository(session).update_account(
        user_id=current_user.id, account_id=id, update_data=update_data)

    # Decode password to display in update data
    account_db.password = security.decode_password(
        password_encode=account_db.password, secret_key=secret_key)

    return account_db
