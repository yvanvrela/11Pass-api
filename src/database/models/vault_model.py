from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.utils.database import Base 


class VaultModel(Base):
    __tablename__ = 'vaults'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=40), index=True)
    description = Column(String(length=240))
    icon_type = Column(String(length=260))
    user_id=Column(Integer, ForeignKey(column='users.id'))

    # Is the referencing a collection of items represented by the child.
    accounts = relationship('AccountModel')
    cards = relationship('CardModel')
