from sqlalchemy import Column, ForeignKey, Integer, String

from src.utils.database import Base 


class CardModel(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=40), unique=True, index=True)
    number = Column(String(length=40), unique=True, index=True)
    type = Column(String(length=40), index=True)
    bank = Column(String(length=40), index=True)
    ccv = Column(String(length=10), unique=True)
    expiration = Column(String(length=10))
    pin = Column(String(length=10))
    description = Column(String(length=240))
    vault_id = Column(Integer, ForeignKey(column='vaults.id'))
