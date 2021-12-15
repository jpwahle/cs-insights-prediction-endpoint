"""Middlware that allows for protection of endoints using JWTs"""
from datetime import datetime, timedelta
from typing import Optional

import jwt
import pydantic
import requests
from decouple import config  # type: ignore
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from nlp_land_prediction_endpoint.models.model_token_data import TokenData
from nlp_land_prediction_endpoint.models.model_user import UserModel

jwt_scheme = OAuth2PasswordBearer(tokenUrl=config("AUTH_TOKEN_ROUTE"))

SECRET = config("JWT_SECRET")
ALG = config("JWT_ALG")


def create_token(user: TokenData, expires_delta: timedelta = None) -> str:
    """Creates a JWT given a user as TokenData.
    This will use the JWT_SECRET and JWT_ALG as defined in the .env variable.

    Arguments:
        user -- TokenData object containing at minimum the email
        expires_delta -- time offset from NOW when the token will expire

    Returns:
        str: a valid JWT as a string
    """
    data = user.dict().copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=30)
    data.update({"sub": user.email})
    data.update({"exp": expires})
    token = jwt.encode(data, SECRET, ALG)
    return token


def authenticate_user(user: UserModel) -> Optional[TokenData]:
    """Checks whether the supplied UserModel contains valid
    credentials. This is done by going through the authorization
    endpoint specified in AUTH_LOGIN_ROUTE at the host AUTH_LOGIN_PROVIDER.

    Arguments:
        user: a user model to authenticate

    Returns:
        Optional[TokenData]: If the authentication was successfull a TokenData object;
        None otherwise
    """
    login_provider = config("AUTH_LOGIN_PROVIDER")
    login_route = config("AUTH_LOGIN_ROUTE")
    try:
        r = requests.post(
            f"{login_provider}{login_route}",
            data=user.dict(),
            headers={"content-type": "application/json"}
        )
        if r.status_code == status.HTTP_200_OK:
            return TokenData(**r.json())
        else:
            return None
    except requests.RequestException:
        return None


async def get_current_user(token: str = Depends(jwt_scheme)) -> UserModel:
    """Returns the current user given a valid JWT

    Arguments:
        token: a bearer token taken from the "Authorization" header

    Returns:
        UserModel: If the token is valid a UserModel with at least an email;
        None otherwise
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=[ALG])
        user = UserModel(**decoded_token)
    except (jwt.exceptions.InvalidTokenError, pydantic.ValidationError):
        raise credentials_exception
    return user
