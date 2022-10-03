from pydantic import BaseModel, Field
from src.mixins.models_mixin import IDMixin, UserIDReferenceMixin, VaultIDReferenceMixin, NameMixin, UsernameMixin, EmailMixin, PasswordMixin, DescriptionMixin, IconTypeMixin


class AccountBase(NameMixin, UsernameMixin, EmailMixin, PasswordMixin, DescriptionMixin, IconTypeMixin, BaseModel):
    page_url:  str | None = Field(
        ...,
        max_length=260,
        example='https://www.facebook.com/',
    )


class AccountOut(IDMixin, UserIDReferenceMixin, VaultIDReferenceMixin, AccountBase):
    pass
