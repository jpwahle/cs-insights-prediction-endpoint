"""Model used for JWT-responses"""
from pydantic import BaseModel


class TokenModel(BaseModel):
    """Model used for tokens"""

    acces_token: str
    token_type: str
