"""This module implements the settings as well as the default settings"""
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """Settings class according to pydantic"""

    auth_backend_version: Optional[str] = "v0"
    implemented_models: Optional[list] = [
        {"lda": ["cs_insights_prediction_endpoint.models.lda_model", "LDAModel"]}
    ]
    node_type: Optional[str] = "SECONDARY"
    remote_host_db_name: Optional[str] = "remote_hosts"
    model_db_name: Optional[str] = "models"
    auth_token_route: Optional[str] = "/auth/service"
    auth_backend_login_route: Optional[str] = "/auth/login/service"
    jwt_sign_alg: Optional[str] = "HS256"
    jwt_token_expiration_minutes: Optional[int] = 30

    jwt_secret: SecretStr
    mongo_user: SecretStr
    mongo_password: SecretStr
    mongo_db: str
    mongo_host: str
    auth_backend_url: str

    class Config:
        """Configuration for settings"""

        case_sensitive = False
        secrets_dir = "/run/secrets"  # for production and docker secrets


@lru_cache()
def get_settings() -> Settings:
    """Return the Settings object"""
    return Settings()
