from pydantic import BaseModel
from src.mixins.models_mixin import UserIDReferenceMixin, DescriptionMixin, IDMixin, NameMixin, IconTypeMixin


class VaultBase(NameMixin, DescriptionMixin, IconTypeMixin, BaseModel):
    pass


class VaultOut(IDMixin, UserIDReferenceMixin, VaultBase):
    pass
