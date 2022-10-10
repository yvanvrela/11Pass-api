from pydantic import BaseModel, Field
from src.mixins.models_mixin import UserIDReferenceMixin, DescriptionMixin, IDMixin, NameMixin, IconTypeMixin


class VaultBase(NameMixin, DescriptionMixin, IconTypeMixin, UserIDReferenceMixin, BaseModel):
    pass


class VaultOut(IDMixin,  VaultBase):
    class Config:
        orm_mode = True
