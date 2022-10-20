from pydantic import BaseModel, Field, EmailStr
from src.mixins.models_mixin import EmailMixin, IDMixin, PasswordMixin, UsernameMixin


class UserBase(UsernameMixin, EmailMixin, BaseModel):

    profile_url: str | None = Field(
        ...,
        max_length=260,
        example='https://www.images.com/sdafjhasfasd',
    )

    class Config:
        orm_mode = True


class UserOut(IDMixin, UserBase):
    class Config:
        orm_mode = True


class UserLogin(UserBase, PasswordMixin):
    class Config:
        orm_mode = True
