from sqlalchemy import Column, ForeignKey, Integer, String

from utils.database import Base as BaseModel


class AccountModel(BaseModel):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=40), unique=True, index=True)
    username = Column(String(length=40), index=True)
    email = Column(String(length=50), index=True)
    password = Column(String(length=64))
    description = Column(String(length=240))
    page_url = Column(String(length=260))
    icon_url = Column(String(length=260))
    account_id = Column(Integer, ForeignKey(column='vaults.id'))
