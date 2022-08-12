"""Module for getting the version of NLP-Land-backend"""
import os

import requests

from cs_insights_prediction_endpoint.utils import settings as Settings

settings = Settings.get_settings()


# XXX-TN Maybe pass settings object instead of using Settings.get_settings()
def get_backend_version() -> None:
    """Utility function which provides the correct version for the backend"""
    if settings.auth_backend_version is None:
        if settings.auth_backend_url.endswith("{version}"):
            AUTH_BACKEND_VERSION_ROUTE = settings.auth_backend_url.format(version="version")
            version_response = requests.get(AUTH_BACKEND_VERSION_ROUTE)
            version = version_response.json()
            if "__v" in version:
                AUTH_BACKEND_VERSION = "v" + str(version["__v"])
                os.environ["AUTH_BACKEND_VERSION"] = AUTH_BACKEND_VERSION
                new_backend_url = settings.auth_backend_url.format(version=AUTH_BACKEND_VERSION)
                os.environ["AUTH_BACKEND_URL"] = new_backend_url
    else:
        new_backend_url = settings.auth_backend_url.format(version=settings.auth_backend_version)
        os.environ["AUTH_BACKEND_URL"] = new_backend_url
