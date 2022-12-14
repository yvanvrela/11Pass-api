from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.infra.database.models.user_model import UserModel
from src.infra.schemas import user_schema


class UserRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, user: user_schema.UserLogin):
        user_bd = UserModel(
            username=user.username,
            email=user.email,
            password=user.password,
            secret_key=user.secret_key,
            profile_url=user.profile_url,
        )
        self.session.add(user_bd)
        self.session.commit()
        self.session.refresh(user_bd)
        return user_bd

    def get_user(self, user_email: str) -> UserModel:
        """Get user by email or username

        This is repository function search a user by email or username.

        Args:

            user_email (str): User email or username.

        Returns:

            UserModel: usermodel information.
        """
        return self.session.query(UserModel).filter(
            or_(
                UserModel.email == user_email,
                UserModel.username == user_email
            )
        ).first()

    def get_user_by_id(self, user_id: int) -> UserModel:
        user_db = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        return user_db

    def update_user(self, user_id: int, update_data: user_schema.UserLogin) -> UserModel:
        """Update a user

        This is repository function update the user by user data and id.

        Args:

            user_id (int): User id.
            update_data (user_schema.UserLogin): user information to update.

        Returns:

            UserModel: usermodel information.
        """
        user_db = self.get_user_by_id(user_id)

        user_db.email = update_data.email
        user_db.username = update_data.username
        user_db.password = update_data.password
        user_db.profile_url = update_data.profile_url

        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)
        return user_db

    def delete_user(self, user_id: int) -> UserModel:
        """Delete a user

        This is repository function delete the user by the user id.

        Args:

            user_id (int): User id.

        Returns:

            UserModel: usermodel delete infomation.
        """

        user_db = self.get_user_by_id(user_id)

        self.session.delete(user_db)
        self.session.commit()
        return user_db
