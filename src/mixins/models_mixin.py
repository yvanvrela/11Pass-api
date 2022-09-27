from pydantic import BaseModel, Field, EmailStr


class IDMixin(BaseModel):
    id: int = Field(
        ...,
        ge=1,
        description='Unique ID of the document.',
        example='1',
    )


class UserIDReferenceMixin(BaseModel):
    user_id: int = Field(
        ...,
        ge=1,
        title='User id reference',
        example=1,
    )


class VaultIDReferenceMixin(BaseModel):
    vault_id: int = Field(
        ...,
        ge=1,
        title='Vault id reference',
        example=1,
    )


class EmailMixin(BaseModel):
    email: EmailStr = Field(...)


class NameMixin(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=40,
        description='Unique name of the document.',
        example='Social',
    )


class UsernameMixin(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=40,
        example='username123',
    )


class DescriptionMixin(BaseModel):
    description: str | None = Field(
        ...,
        min_length=1,
        max_length=240,
        example='This is a description.',
    )


class IconTypeMixin(BaseModel):
    icon_type: str = Field(
        min_length=1,
        max_length=260,
        example='name-icon',
    )


class PasswordMixin(BaseModel):
    password: str = Field(
        ...,
        min_length=12,
        max_length=64,
        example='Mypassword123.'
    )
