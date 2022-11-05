from fastapi import APIRouter, Depends, Body, Path, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from src.core import security
from src.infra.schemas import account_schema
from src.infra.database.models import user_model, vault_model, account_model
from src.infra.database.repositories.account_repository import AccountRepository
from src.infra.database.repositories.vault_repository import VaultRepository
from src.infra.database.config.database import get_db
from src.utils.auth_utils import get_current_user


router = APIRouter()


@router.post(path='/',
             status_code=status.HTTP_201_CREATED,
             response_model=account_schema.AccountOut,
             summary='Add a new account to the app'
             )
def create_account(
    account: account_schema.AccountCreate = Body(...,),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Add a new account to the app

    This is the path operation add a new account to the app.

    Args:

        Account (json): These are the data to add. The example in the request body.
        Token (str)

    Raises:

        HTTPException(json): If it is not a valid user id.
            Code: 404,
            detail:User not found.

        HTTPException(json): If it is not a valid vault id.
            Code: 404,
            detail:Vault not found.

        HTTPException(json): If it already exists account name.
            Code: 400,
            detail:Account name already exists.

    Returns:

        json: Account data.
    """
    # Verify user
    if current_user.id != account.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.',
        )

    # Verify vault
    vault_reference = VaultRepository(session).get_vault_by_id(
        vault_id=account.vault_id, user_id=account.user_id)
    if not vault_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vault not found.',
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

    # Decode password to display in update data
    account_db.password = security.decode_password(
        password_encode=account_db.password, secret_key=secret_key)

    return account_db


@router.get(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=account_schema.AccountOut,
            summary='Find account by ID',
            )
def get_account(
    id: int = Path(...,
                   gt=0,
                   example=1,
                   description='ID of account to return.',
                   ),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> account_schema.AccountOut:
    """Find account by ID

    This path operation get account by ID, and return a single account.

    Args:

        id (int): This is the account id.
        Token (str)

    Raises:

        HTTPException(json): If it is not a valid account id.
            Code: 404,
            detail:Account not found.

    Returns:

        json: Account data.
    """
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
            summary='Get a list with all accounts.',
            )
def get_accounts(
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> List[account_schema.AccountOut]:
    """Get a list with all accounts.

    This is the path operation to return a list of all accounts in the app.

    Args:

        Token (str)

    Raises:

        HTTPException(json): If it is not accounts.
            Code: 404,
            detail:Accounts not found.

    Returns:

        List[json]: Accounts data.
    """
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
            summary='Update an existing account',
            )
def update_account(
    id: int = Path(...,
                   gt=0,
                   example=1,
                   description='ID of account to update.',
                   ),
    update_data: account_schema.AccountCreate = Body(...,),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> account_schema.AccountOut:
    """Update an existing account

    This is the path operation that updates an existing account in the app.

    Args:

        id (int): This is the account id.
        update_data(json): These are the data to update.
        Token (str)

    Raises:

        HTTPException(json): If it is not a valid user id.
            Code: 404,
            detail:User not found.

        HTTPException(json): If it is not a valid vault id.
            Code: 404,
            detail:Vault not found.

        HTTPException(json): If it already exists account name.
            Code: 400,
            detail:Account name already exists.

    Returns:

        json: Account data.
    """
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

    # Decode secret key
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


@router.delete(path='/{id}',
               status_code=status.HTTP_200_OK,
               response_model=account_schema.AccountOut,
               summary='Delete an account',
               )
def delete_account(
    id: int = Path(...,
                   gt=0,
                   example=1,
                   description='Account ID to delete',
                   ),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> account_schema.AccountOut:
    """Delete an account

    This is the path operation that deletes an existing account in the app.

    Args:

        id (int): This is the account id.
        Token (str)

    Raises:

        HTTPException(json): If it is not account.
            Code: 404,
            detail:Account not found.

    Returns:
        json: Account data.
    """
    # Verify account reference by id
    account_reference = AccountRepository(session).get_account_by_id(
        account_id=id, user_id=current_user.id)
    if not account_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Account not found.'
        )

    # Delete the account
    account_db = AccountRepository(session).delete_account(
        account_id=id, user_id=current_user.id)

    # Decode secret key
    secret_key = security.decode_secret_key(
        secret_key_encode=current_user.secret_key)

    # Decode password to display in update data
    account_db.password = security.decode_password(
        password_encode=account_db.password, secret_key=secret_key)

    return account_db
