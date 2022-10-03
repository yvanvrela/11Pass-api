from sqlalchemy import Column, ForeignKey, Integer, String

from src.infra.database.config.database import Base 


class CardModel(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=40), index=True)
    number = Column(String(length=40), index=True)
    type = Column(String(length=40), index=True)
    bank = Column(String(length=40), index=True)
    ccv = Column(String(length=10))
    expiration = Column(String(length=10))
    pin = Column(String(length=10))
    description = Column(String(length=240))
    vault_id = Column(Integer, ForeignKey(column='vaults.id'))
    user_id=Column(Integer, ForeignKey(column='users.id'))
    
