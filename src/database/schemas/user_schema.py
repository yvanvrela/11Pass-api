from pydantic import BaseModel, Field, EmailStr
from mixins.models_mixin import IDMixin


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=40,
        example='Juan',
    )

    email: EmailStr = Field(...)

    profile_url: str = Field(
        max_length=260, example='https://www.images.com/sdafjhasfasd')

    secret_key: str | None = Field(
        ...,
        min_length=20,
        max_length=64,
        example='c89aac42b1tE0eae7V7e'
    )


class UserOut(IDMixin, UserBase):
    pass


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=12,
        max_length=64,
        example='Mypassword123.'
    )
