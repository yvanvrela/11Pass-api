from fastapi import APIRouter, Depends, Body, Path, HTTPException, status
from sqlalchemy.orm import Session
from src.infra.schemas import user_schema
from src.infra.database.models import user_model
from src.infra.database.repositories.user_repository import UserRepository
from src.infra.providers import password_provider
from src.infra.database.config.database import get_db
from src.utils.auth_utils import get_current_user


router = APIRouter()


@router.get(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=user_schema.UserOut,
            summary='Get a user',
            )
def get_user(
    id: int = Path(..., gt=0, example=1,),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Get a user

    This path operation show the user by the id in the database.

    Args:

        id (int): This is the user id.

    Returns:

        Usermodel: usermodel user information.
    """
    user_reference = UserRepository(session).get_user_by_id(id)
    if not user_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    user_db = user_reference
    return user_db


@router.put(path='/{id}',
            status_code=status.HTTP_200_OK,
            response_model=user_schema.UserOut,
            summary='Update a user',
            )
def update_user(
    id: int = Path(..., gt=0, example=1,),
    update_data: user_schema.UserLogin = Body(...,),
    current_user: user_model.UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Update a user

      This path operation updates the user by the id in the database.

      Args:

        id (int): This is the user id.
        update_data (user_schema.UserLogin): This is the User update data.
        current_user (Token): This is the Token user.

      Returns:

        UserModel: usermodel user information updated.
    """
    # Verify user
    user_reference = UserRepository(session).get_user_by_id(user_id=id)
    if not user_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    # Verify email duplicate in db
    if update_data.email != user_reference.email:
        user_email_reference = UserRepository(
            session).get_user(update_data.email)
        if user_email_reference:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered.'
            )

    # Verify username duplicate in db
    if update_data.username != user_reference.username:
        username_reference = UserRepository(
            session).get_user(update_data.username)
        if username_reference:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already registered.'
            )

    # Hash password
    update_data.password = password_provider.hash_password(
        update_data.password
    )

    user_db = UserRepository(session).update_user(
        user_id=id, update_data=update_data)

    return user_db


@router.delete(path='/{id}',
               status_code=status.HTTP_200_OK,
               response_model=user_schema.UserOut,
               summary='Delete a user',
               )
def delete_user(
    id: int = Path(..., gt=0, example=1),
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Delete a user

    This path operation delete a user by id in the database.

    Args:

        id (int): This is the user id.
        token (str): This is the bearer token of the user.

    Returns:

        status_code: 204
    """
    # Verify user
    user_reference = UserRepository(session).get_user_by_id(user_id=id)
    if not user_reference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    # Verify current user
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    user_db = UserRepository(session).delete_user(user_id=id)

    return user_db
