"""Model used for JWT-responses"""
from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    """Model used for JWT-responses

    Attributes:
        acces_token (str): the actual token
        token_type (str): this will always be bearer
    """

    acces_token: str = Field(...)
    token_type: str = Field(...)
