"""Middlware that allows for protection of endoints using JWTs"""
from datetime import datetime, timedelta
from typing import Optional

import jwt
import pydantic
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from nlp_land_prediction_endpoint.models.model_token_data import TokenData
from nlp_land_prediction_endpoint.models.model_user import UserModel
from nlp_land_prediction_endpoint.models.model_user_login import UserLoginModel
from nlp_land_prediction_endpoint.utils.settings import Settings, get_settings

token_url = get_settings().AUTH_TOKEN_ROUTE
jwt_scheme = OAuth2PasswordBearer(tokenUrl=token_url)


def encode_token(data: dict, settings: Settings) -> str:
    """Encodes supplied data into an JWT
    Arguments:
        data (dict): Dictionary containing some data (e.g., a UserModel dict)
        settings (Settings): Settings object; populated by .env file

    Returns:
        str: a valid JWT token
    """
    SECRET = settings.JWT_SECRET
    ALG = settings.JWT_SIGN_ALG
    return str(jwt.encode(data, SECRET, ALG))


def decode_token(token: str, settings: Settings) -> TokenData:
    """Decodes a supplied JWT into a TokenData model
    (decoding exception should be catched on function call)

    Arguments:
        token (str): a (possibly invalid) JWT token
        settings (Settings): Settings object; populated by .env file

    Returns:
        TokenData: a TokenData model representing the decoded JWT token
    """
    SECRET = settings.JWT_SECRET
    ALG = settings.JWT_SIGN_ALG
    return TokenData(**jwt.decode(token, SECRET, [ALG]))


def create_token(user: UserModel, settings: Settings, expires_delta: timedelta = None) -> str:
    """Creates a JWT given a user as TokenData.
    This will use the JWT_SECRET and JWT_SIGN_ALG as defined in the .env variable.

    Arguments:
        user (TokenData): TokenData object containing at minimum the email
        expires_delta (timedelta): time offset from NOW when the token will expire

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
    token = encode_token(data, settings)
    return token


def authenticate_user(user: UserLoginModel, settings: Settings) -> Optional[UserModel]:
    """Checks whether the supplied UserModel contains valid
    credentials. This is done by going through the authorization
    endpoint specified in AUTH_LOGIN_ROUTE at the host AUTH_LOGIN_PROVIDER.

    Arguments:
        user (UserModel): a user model to authenticate
        settings (Settings): Settings object; populated by .env file

    Returns:
        Optional[UserModel]: If the authentication was successful a UserModel object;
        None otherwise
    """
    login_provider = settings.AUTH_BACKEND_URL
    login_route = settings.AUTH_BACKEND_LOGIN_ROUTE
    try:
        r = requests.post(
            f"{login_provider}{login_route}",
            data=user.dict(),
            headers={"content-type": "application/json"},
        )
        if r.status_code == status.HTTP_200_OK:
            return UserModel(**r.json())
        else:
            return None
    except requests.RequestException:
        return None


async def get_current_user(
    token: str = Depends(jwt_scheme), settings: Settings = Depends(get_settings)
) -> UserModel:
    """Returns the current user given a valid JWT

    Arguments:
        token (str): a bearer token taken from the "Authorization" header

    Returns:
        UserModel: If the token is valid a UserModel with at least an email;
        None otherwise
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = decode_token(token, settings)
        user = UserModel(**decoded_token.dict())
    except (jwt.exceptions.InvalidTokenError, pydantic.ValidationError):
        raise credentials_exception
    return user
