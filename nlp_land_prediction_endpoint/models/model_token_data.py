"""Model used for JWT-token data"""
from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    """Model used for Token data (the payload of the token)
    This contains a subset of attributs from the UserModel

    Attributes:
        email: email of the user
        fullname: fullname of the user
        isAdmin: flag indicating whether it is a admin
        isActive: flag indicating whether the user is still active
    """

    # XXX-TN change isAdmin to groups
    # TODO-TN isActive is currently getting ignored

    email: Optional[str] = None
    fullname: Optional[str] = None
    isAdmin: Optional[bool] = False
    isActive: Optional[bool] = False
