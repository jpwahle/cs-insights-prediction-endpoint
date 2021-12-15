"""Model used for defining a user; Should be equivilent to the
definition in the NLP-Land-Backend
"""
from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    """The model for a user. Should be identical to the NLP-Land-backend

    Arguments:
        BaseModel(Any): Base class of FastAPI modesl.
    """

    email: str = Field(...)
    password: Optional[str] = Field(...)
    fullname: Optional[str] = Field()
    token: Optional[str] = Field()
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
