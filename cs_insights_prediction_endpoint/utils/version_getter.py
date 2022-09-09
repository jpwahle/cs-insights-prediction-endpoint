"""Module for getting the version of cs-insights-backend"""
import os

import requests

from cs_insights_prediction_endpoint.utils import settings as Settings  # noqa: N812

settings = Settings.get_settings()


# XXX-TN Maybe pass settings object instead of using Settings.get_settings()
def get_backend_version() -> None:
    """Utility function which provides the correct version for the backend"""
    if settings.auth_backend_version is None:
        if settings.auth_backend_url.endswith("{version}"):
            auth_backend_version_route = settings.auth_backend_url.format(version="version")
            version_response = requests.get(auth_backend_version_route)
            version = version_response.json()
            if "__v" in version:
                auth_backend_version = "v" + str(version["__v"])
                os.environ["AUTH_BACKEND_VERSION"] = auth_backend_version
                new_backend_url = settings.auth_backend_url.format(version=auth_backend_version)
                os.environ["AUTH_BACKEND_URL"] = new_backend_url
    else:
        new_backend_url = settings.auth_backend_url.format(version=settings.auth_backend_version)
        os.environ["AUTH_BACKEND_URL"] = new_backend_url
