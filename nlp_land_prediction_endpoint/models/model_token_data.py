"""Model used for JWT-token data"""
from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    """Model used for Token data (the payload of the token)"""

    email: Optional[str] = None
    fullname: Optional[str] = None
    isAdmin: Optional[bool] = False
    isActive: Optional[bool] = False
