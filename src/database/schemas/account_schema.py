from pydantic import BaseModel, Field
from mixins.models_mixin import IDMixin, NameMixin, UsernameMixin, EmailMixin, PasswordMixin, DescriptionMixin, IconTypeMixin


class AccountBase(NameMixin, UsernameMixin, EmailMixin, PasswordMixin, DescriptionMixin, IconTypeMixin, BaseModel):
    page_url:  str | None = Field(
        ...,
        max_length=260,
        example='https://www.facebook.com/',
    )


class AccountOut(IDMixin, AccountBase):
    vault_id: int = Field(
        ...,
        ge=1,
        title='Vault id reference',
        example=1,
    )
