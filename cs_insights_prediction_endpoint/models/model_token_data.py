"""Model used for JWT-token data"""
from typing import Optional

from pydantic import Field

from cs_insights_prediction_endpoint.models.model_user import user_model


class token_data(user_model):
    """Model used for Token data (the payload of the token)
    This contains a subset of attributs from the user_model

    Attributes:
        email (str): email of the user
        fullname (str): fullname of the user
        is_admin (Optional[bool]): flag indicating whether it is a admin
        is_active (Optional[bool]): flag indicating whether the user is still active

        sub (str): subject of the JWT (email)
        exp (str): expiration date of the JWT
    """

    # JWT specific attributes
    sub: Optional[str] = Field(default=None)  # Subject (unique identifier)
    exp: Optional[str] = Field(default=None)  # Expiration (expiration date)
