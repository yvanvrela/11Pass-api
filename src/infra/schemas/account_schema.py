from pydantic import BaseModel, Field
from src.mixins.models_mixin import IDMixin, UserIDReferenceMixin, VaultIDReferenceMixin, NameMixin, UsernameMixin, EmailMixin, PasswordMixin, DescriptionMixin, IconTypeMixin


class AccountBase(NameMixin, UsernameMixin, EmailMixin, DescriptionMixin, IconTypeMixin, VaultIDReferenceMixin, UserIDReferenceMixin, BaseModel):
    page_url:  str | None = Field(
        ...,
        max_length=260,
        example='https://www.facebook.com/',
    )


class AccountCreate(AccountBase):
    password: str = Field(
        ...,
        min_length=1,
        max_length=64,
        example='Mypassword'
    )

    class Config:
        orm_mode = True


class AccountOut(IDMixin, AccountCreate, AccountBase):
    class Config:
        orm_mode = True
