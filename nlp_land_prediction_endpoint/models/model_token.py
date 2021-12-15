"""Model used for JWT-responses"""
from pydantic import BaseModel


class TokenModel(BaseModel):
    """Model used for JWT-responses

    Attributes:
        acces_token: the actual token
        token_type: this will always be bearer
    """

    acces_token: str
    token_type: str
