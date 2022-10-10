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
             summary='Create a vault',
             )
def create_vault(
    vault: vault_schema.VaultBase,
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
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


@router.get(path='/',
            status_code=status.HTTP_200_OK,
            response_model=List[vault_schema.VaultOut],
            summary='Get all user vaults',
            )
def get_vaults(
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    vaults_db = VaultRepository(session).get_vaults(user_id=current_user.id)
    if not vaults_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vaults not found',
        )

    return vaults_db
