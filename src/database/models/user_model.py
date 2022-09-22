from sqlalchemy import Column, Integer, String

from utils.database import Base as BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=40), unique=True, index=True)
    email = Column(String(length=50), unique=True, index=True)
    password = Column(String(length=64))
    secret_key = Column(String(length=30), index=True)
    profile_url = Column(String(length=260))
