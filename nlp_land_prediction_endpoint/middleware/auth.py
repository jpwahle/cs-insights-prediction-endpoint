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
    """Creats a JWT Token"""
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
    """Executes the login procedure and returns:
    - the token on sucess
    - None otherwise
    """
    login_provider = config("AUTH_LOGIN_PROVIDER")
    login_route = config("AUTH_LOGIN_ROUTE")
    if login_provider == "testing":
        return TokenData(
            email="admin@nlp-land-prediction-backend.com",
            fullname="admin",
            isAdmin=True,
            isActive=True,
        )
    else:
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
    """Returns the current user based on the supplied jwt-token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=[ALG])
        user = UserModel(**decoded_token)
        # if email is None:
        #     raise credentials_exception
    except (jwt.exceptions.InvalidTokenError, pydantic.ValidationError):
        raise credentials_exception
    return user
