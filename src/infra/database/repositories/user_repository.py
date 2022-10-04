from sqlalchemy import select
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

    def get_user_by_email(self, user_email: str) -> UserModel:
        query = select(UserModel).where(
            UserModel.email == user_email)
        return self.session.execute(query).first()
