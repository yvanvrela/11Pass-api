from pydantic import BaseModel, Field, EmailStr
from src.mixins.models_mixin import IDMixin, PasswordMixin, UsernameMixin


class UserBase(BaseModel):
    email: EmailStr = Field(...)

    profile_url: str | None = Field(
        ...,
        max_length=260,
        example='https://www.images.com/sdafjhasfasd',
    )

    secret_key: str | None = Field(
        ...,
        min_length=20,
        max_length=64,
        example='c89aac42b1tE0eae7V7e'
    )


class UserOut(IDMixin, UserBase):
    pass


class UserLogin(UserBase, PasswordMixin):
    pass
