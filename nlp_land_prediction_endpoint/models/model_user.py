"""Model used for defining a user; Should be equivilent to the
definition in the NLP-Land-Backend
"""
from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    """The model for a user. Should be identical to the NLP-Land-backend

    Arguments:
        BaseModel(Any): Base class of FastAPI modesl.

    Attributes:
        email (str): email of the user
        password (str): password of the user
        fullname (Optional[str]): fullname of the user
        isAdmin (Optional[bool]): flag indicating whether it is a admin
        isActive (Optional[bool]): flag indicating whether the user is still active
    """

    email: str = Field(...)
    password: str = Field(...)
    fullname: Optional[str] = Field()
    isAdmin: Optional[bool] = Field()
    isActive: Optional[bool] = Field()

    class Config:
        """Configuration for UserModel"""

        schema_extra = {
            "example": {
                "email": "admin@nlp.de",
                "password": "12345",
                "fullname=": "admin",
                "token": None,
                "isAdmin": True,
                "isActive": True,
            }
        }
