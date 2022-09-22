from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from utils.database import Base as BaseModel


class VaultModel(BaseModel):
    __tablename__ = 'vaults'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=40), unique=True, index=True)
    description = Column(String(length=240))
    icon_type = Column(String(length=260))

    # Is the referencing a collection of items represented by the child.
    accounts = relationship('AccountModel')
