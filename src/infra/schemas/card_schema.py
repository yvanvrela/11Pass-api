from pydantic import BaseModel, Field
from src.mixins.models_mixin import IDMixin, UserIDReferenceMixin, VaultIDReferenceMixin, NameMixin, DescriptionMixin


class CardModel(NameMixin, DescriptionMixin, BaseModel):
    number: str = Field(
        ...,
        min_length=1,
        max_length=40,
        example='123-456-789-101',
    )

    type: str = Field(
        ...,
        min_length=1,
        max_length=40,
        example='Mastercard',
    )

    bank: str = Field(
        ...,
        min_length=1,
        max_length=40,
        example='Atlas',
    )

    ccv: str = Field(
        ...,
        min_length=3,
        max_length=10,
        example='000',
    )

    expiration: str = Field(
        ...,
        min_length=1,
        max_length=10,
        example='17/23',
    )

    pin: str = Field(
        ...,
        min_length=1,
        max_length=10,
        example='1234',
    )


class CardOut(IDMixin, VaultIDReferenceMixin, UserIDReferenceMixin, CardModel):
    pass
