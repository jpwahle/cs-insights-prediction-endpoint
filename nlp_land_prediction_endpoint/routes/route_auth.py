"""This module implements the authentication endpoint"""
from datetime import timedelta

from decouple import config  # type: ignore
from fastapi import APIRouter, Depends, HTTPException, status

from nlp_land_prediction_endpoint.middleware.auth import (
    authenticate_user,
    create_token,
    get_current_user,
)
from nlp_land_prediction_endpoint.models.model_token import TokenModel
from nlp_land_prediction_endpoint.models.model_token_data import TokenData
from nlp_land_prediction_endpoint.models.model_user import UserModel
from nlp_land_prediction_endpoint.models.model_user_login import UserLoginModel

router = APIRouter()

TIME_DELTA = config("JWT_TOKEN_EXPIRATION_MINUTES", cast=int, default=30)


@router.post("/login", response_description="Trigger login procedure", response_model=TokenModel)
async def login(user: UserLoginModel) -> TokenModel:
    """Login routine

    Arguments:
        user (UserModel): user credentials at least (email, password)

    Returns:
        TokenModel: a JWT given a valid user from the NLP-Land-Backend
    """
    auth_user = authenticate_user(user)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expiration = timedelta(minutes=TIME_DELTA)
    token = create_token(auth_user, token_expiration)
    return TokenModel(access_token=token, token_type="bearer")


@router.post("/refresh", response_description="Trigger login procedure", response_model=TokenModel)
async def refresh(user: UserModel = Depends(get_current_user)) -> TokenModel:
    """Generates a new token without the need of logging in again

    Arguments:
        user(UserModel): a user depending on the supplied token

    Returns:
        TokenModel: a JWT given a valid user from the NLP-Land-Backend
    """
    token_expiration = timedelta(minutes=TIME_DELTA)
    token = create_token(TokenData(**user.dict()), token_expiration)
    return TokenModel(access_token=token, token_type="bearer")
