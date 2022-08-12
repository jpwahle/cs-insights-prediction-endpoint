"""This module implements the settings as well as the default settings"""
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class according to pydantic"""

    AUTH_BACKEND_VERSION: Optional[str] = "v0"
    IMPLEMENTED_MODELS: Optional[list] = [
        {"lda": ["cs_insights_prediction_endpoint.models.lda_model", "LDAModel"]}
    ]
    NODE_TYPE: Optional[str] = "SECONDARY"
    REMOTE_HOST_DB_NAME: Optional[str] = "remote_hosts"
    MODEL_DB_NAME: Optional[str] = "models"
    AUTH_TOKEN_ROUTE: Optional[str] = "/auth/service"
    AUTH_BACKEND_LOGIN_ROUTE: Optional[str] = "/auth/login/service"
    JWT_SIGN_ALG: Optional[str] = "HS256"
    JWT_TOKEN_EXPIRATION_MINUTES: Optional[int] = 30

    AUTH_BACKEND_URL: str
    JWT_SECRET: str
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DB: str
    MONGO_HOST: str

    class Config:
        """Configuration for settings"""

        secrets_dir = "/run/secrets"  # for production and docker secrets


@lru_cache()
def get_settings() -> Settings:
    """Return the Settings object"""
    return Settings()
