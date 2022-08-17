"""Model used for defining a user; Should be equivilent to the
definition in the NLP-Land-Backend
"""
from pydantic import BaseModel, Field


class user_login_model(BaseModel):
    """The model for a user login. This model contains only
    the fields that are submitted on a login

    Arguments:
        BaseModel(Any): Base class of FastAPI modesl.

    Attributes:
        email (str): email of the user
        password (str): password of the user
    """

    email: str = Field(...)
    password: str = Field(...)

    class Config:
        """Configuration for UserModel"""

        schema_extra = {
            "example": {
                "email": "admin@nlp.de",
                "password": "12345",
            }
        }
