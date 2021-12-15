"""Model used for JWT-token data"""
from typing import Optional

from pydantic import BaseModel, Field


class TokenData(BaseModel):
    """Model used for Token data (the payload of the token)
    This contains a subset of attributs from the UserModel

    Attributes:
        email (str): email of the user
        fullname (str): fullname of the user
        isAdmin (Optional[bool]): flag indicating whether it is a admin
        isActive (Optional[bool]): flag indicating whether the user is still active
    """

    # XXX-TN change isAdmin to groups
    # TODO-TN isActive is currently getting ignored

    email: str = Field(...)
    fullname: Optional[str] = Field(default=None)
    isAdmin: Optional[bool] = Field(default=False)
    isActive: Optional[bool] = Field(default=False)
