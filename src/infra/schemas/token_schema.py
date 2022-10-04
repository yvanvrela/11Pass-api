from pydantic import BaseModel, Field


class Token(BaseModel):
    """Token

    The token model content a token string and type of the token.

    """
    access_token: str = Field(
        example='asdfasddfasdfagsdf4asdfa',
    )

    token_type: str = Field(
        example='bearer',
    )


class TokenData(BaseModel):
    """Token Data

    The token data model content information by the token.

    """
    user_email: str | None = None
