"""Model used for JWT-responses"""
from pydantic import BaseModel, Field


class token_model(BaseModel):
    """Model used for JWT-responses

    Attributes:
        acces_token (str): the actual token
        token_type (str): this will always be bearer
    """

    access_token: str = Field(...)
    token_type: str = Field(...)
