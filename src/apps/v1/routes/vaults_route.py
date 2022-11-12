from fastapi import APIRouter, Depends, Body, Path, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from src.infra.schemas import vault_schema
from src.infra.database.models import user_model, vault_model
from src.infra.database.repositories.vault_repository import VaultRepository
from src.infra.database.config.database import get_db
from src.utils.auth_utils import get_current_user


router = APIRouter()


@router.post(path='/',
             status_code=status.HTTP_201_CREATED,
             response_model=vault_schema.VaultOut,
             summary='Create a new vault to the app',
             )
def create_vault(
    vault: vault_schema.VaultBase,
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> vault_schema.VaultOut:
    """Create a new vault in the app

    This is the path operation add a new vault to the app.

    Args:

        Vault (json): These are the data to add. The example in the request body.
        Token (str): This is the bearer token.

    Raises:

        HTTPException(json): If it is not a valid user id.
            Code: 404,
            detail: User not found.

        HTTPException(json): If it already exists vault name.
            Code: 400,
            detail: Vault name already exists.

    Returns:

        json: Vault data.
    """
    # Verify user
    if current_user.id != vault.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.',
        )

    # Verify vault name reference
    vault_name_reference = VaultRepository(session).get_vault_by_name(
        vault_name=vault.name, user_id=vault.user_id)
    if vault_name_reference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Vault name already exists.'
        )

    # Add to db
    vault_db = VaultRepository(session).create_vault(vault)

    return vault_db


@router.get(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=vault_schema.VaultOut,
            summary='Find vault by ID',
            )
def get_vault(
    id: int = Path(...,
                   gt=0,
                   example=1,
                   description='ID of vault to return.',
                   ),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> vault_schema.VaultOut:
    """Find vault by ID

    This path operation get vault by ID, and return a single vault.

    Args:

        id (int): This is the vault ID.
        Token (str): This is the bearer token.

    Raises:

        HTTPException(json): If it is not a valid vault ID.
            Code: 404,
            detail: Vault not found.

    Returns:

        json: Vault data.
    """
    vault_db = VaultRepository(session).get_vault_by_id(
        vault_id=id, user_id=current_user.id)
    if not vault_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vault not found',
        )

    return vault_db


@router.get(path='/',
            status_code=status.HTTP_200_OK,
            response_model=List[vault_schema.VaultOut],
            summary='Get a list with all vaults.',
            )
def get_vaults(
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> List[vault_schema.VaultOut]:
    """Get a list with all vaults.

    This is the path operation to return a list of all vaults in the app.

    Args:

        Token (str): This is the bearer token.

    Raises:

        HTTPException(json): If it is not vaults.
            Code: 404,
            detail: Vaults not found.

    Returns:

        List[json]: Vaults data.
    """
    vaults_db = VaultRepository(session).get_vaults(user_id=current_user.id)
    if not vaults_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vaults not found',
        )

    return vaults_db


@router.put(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=vault_schema.VaultOut,
            summary='Update an existing vault',
            )
def update_vault(
    id: int = Path(...,
                   gt=0,
                   example=1,
                   description='ID of vault to update.',
                   ),
    update_data: vault_schema.VaultBase = Body(...,),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> vault_schema.VaultOut:
    """Update an existing vault

    This is the path operation that updates an existing vault in the app.

    Args:

        id (int): This is the vault id.
        update_data(json): These are the data to update.
        Token (str): This is the bearer token.

    Raises:

        HTTPException(json): If it is not a valid vault id.
            Code: 404,
            detail: Vault not found.

        HTTPException(json): If it already exists vault name.
            Code: 400,
            detail: Vault name already exists.

    Returns:

        json: Vault data.
    """
    # Verify vault
    vault_reference = VaultRepository(session).get_vault_by_id(
        vault_id=id, user_id=current_user.id)
    if not vault_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vault not found.',
        )

    # Verify vault name duplicate in db
    if update_data.name != vault_reference.name:
        vault_name_reference = VaultRepository(session).get_vault_by_name(
            vault_name=update_data.name, user_id=current_user.id)
        if vault_name_reference:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Vault name already exists.'
            )

    # Update vault data
    vault_db = VaultRepository(session).update_vault(
        user_id=current_user.id, vault_id=id, update_data=update_data)

    return vault_db


@router.delete(path='/{id}',
               status_code=status.HTTP_200_OK,
               response_model=vault_schema.VaultOut,
               summary='Delete an vault',
               )
def delete_vault(
    id: int = Path(...,
                   gt=0,
                   example=1,
                   description='Vault ID to delete.',
                   ),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> vault_schema.VaultOut:
    """Delete an vault

    This is the path operation that deletes an existing vault in the app.

    Args:

        id (int): This is the vault id.
        Token (str): This is the bearer token.

    Raises:

        HTTPException(json): If it is not vault.
            Code: 404,
            detail: Vault not found.

    Returns:
        json: Vault data.
    """
    # Verify vault reference by id
    vault_reference = VaultRepository(session).get_vault_by_id(
        vault_id=id, user_id=current_user.id)
    if not vault_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vault not found.'
        )

    # Delete the vault
    vault_db = VaultRepository(session).delete_vault(vault_id=id, user_id=current_user.id)

    return vault_db
