"""This module implements the authentication endpoint"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from cs_insights_prediction_endpoint.middleware.auth import (
    authenticate_user,
    create_token,
    get_current_user,
)
from cs_insights_prediction_endpoint.models.model_token import token_model
from cs_insights_prediction_endpoint.models.model_token_data import token_data
from cs_insights_prediction_endpoint.models.model_user import user_model
from cs_insights_prediction_endpoint.models.model_user_login import user_login_model
from cs_insights_prediction_endpoint.utils.settings import Settings, get_settings

router = APIRouter()



@router.post("/login", response_description="Trigger login procedure", response_model=token_model)
async def login(user: user_login_model, settings: Settings = Depends(get_settings)) -> token_model:
    """Login routine

    Arguments:
        user (user_model): user credentials at least (email, password)
        settings (Settings): Settings object; Populatet from .env file

    Returns:
        token_model: a JWT given a valid user from the NLP-Land-Backend
    """
    auth_user = authenticate_user(user, settings)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    TIME_DELTA = settings.jwt_token_expiration_minutes
    token_expiration = timedelta(minutes=TIME_DELTA)
    token = create_token(auth_user, settings, token_expiration)
    return token_model(access_token=token, token_type="bearer")


@router.post("/refresh", response_description="Trigger login procedure", response_model=token_model)
async def refresh(
    user: user_model = Depends(get_current_user), settings: Settings = Depends(get_settings)
) -> token_model:
    """Generates a new token without the need of logging in again

    Arguments:
        user(user_model): a user depending on the supplied token
        settings (Settings): Settings object; Populatet from .env file

    Returns:
        TokenModel: a JWT given a valid user from the NLP-Land-Backend
    """
    TIME_DELTA = settings.jwt_token_expiration_minutes
    token_expiration = timedelta(minutes=TIME_DELTA)
    token = create_token(token_data(**user.dict()), settings, token_expiration)
    return token_model(access_token=token, token_type="bearer")
