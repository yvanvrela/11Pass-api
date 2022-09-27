from pydantic import BaseModel, Field
from mixins.models_mixin import IDMixin


class VaultBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=40,
        example='Social Accounts',
    )

    description: str | None = Field(
        ...,
        min_length=1,
        max_length=240,
        example='This is vault content my social accounts',
    )

    icon_type: str = Field(
        min_length=1,
        max_length=260,
        example='facebook',
    )


class VaultOut(IDMixin, VaultBase):
    pass
