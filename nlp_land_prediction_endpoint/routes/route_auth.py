"""This module implements the authentication endpoint"""
from datetime import timedelta

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
from nlp_land_prediction_endpoint.utils.settings import Settings, get_settings

router = APIRouter()


@router.post("/login", response_description="Trigger login procedure", response_model=TokenModel)
async def login(user: UserLoginModel, settings: Settings = Depends(get_settings)) -> TokenModel:
    """Login routine

    Arguments:
        user (UserModel): user credentials at least (email, password)
        settings (Settings): Settings object; Populatet from .env file

    Returns:
        TokenModel: a JWT given a valid user from the NLP-Land-Backend
    """
    auth_user = authenticate_user(user, settings)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    TIME_DELTA = settings.JWT_TOKEN_EXPIRATION_MINUTES
    token_expiration = timedelta(minutes=TIME_DELTA)
    token = create_token(auth_user, settings, token_expiration)
    return TokenModel(access_token=token, token_type="bearer")


@router.post("/refresh", response_description="Trigger login procedure", response_model=TokenModel)
async def refresh(
    user: UserModel = Depends(get_current_user), settings: Settings = Depends(get_settings)
) -> TokenModel:
    """Generates a new token without the need of logging in again

    Arguments:
        user(UserModel): a user depending on the supplied token
        settings (Settings): Settings object; Populatet from .env file

    Returns:
        TokenModel: a JWT given a valid user from the NLP-Land-Backend
    """
    TIME_DELTA = settings.JWT_TOKEN_EXPIRATION_MINUTES
    token_expiration = timedelta(minutes=TIME_DELTA)
    token = create_token(TokenData(**user.dict()), settings, token_expiration)
    return TokenModel(access_token=token, token_type="bearer")
