"""Model used for defining a user; Should be equivilent to the
definition in the cs-insights-backend
"""
from typing import Optional

from pydantic import BaseModel, Field

# flake8: noqa N815


class UserModel(BaseModel):
    """The model for a user. Should be identical to the cs-insights-backend

    Arguments:
        BaseModel(Any): Base class of FastAPI modesl.

    Attributes:
        email (str): email of the user
        password (str): password of the user
        fullname (Optional[str]): fullname of the user
        is_admin (Optional[bool]): flag indicating whether it is a admin
        is_active (Optional[bool]): flag indicating whether the user is still active
    """

    email: str = Field(...)
    fullname: Optional[str] = Field()
    is_admin: Optional[bool] = Field()
    is_active: Optional[bool] = Field()

    # XXX-TN change is_admin to groups
    # TODO-TN is_active is currently getting ignored

    class Config:
        """Configuration for UserModel"""

        schema_extra = {
            "example": {
                "email": "admin@nlp.de",
                "fullname": "admin",
                "token": None,
                "is_admin": True,
                "is_active": True,
            }
        }
