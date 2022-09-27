from pydantic import BaseModel
from mixins.models_mixin import DescriptionMixin, IDMixin, NameMixin, IconTypeMixin


class VaultBase(NameMixin, DescriptionMixin, IconTypeMixin, BaseModel):
    pass


class VaultOut(IDMixin, VaultBase):
    pass
