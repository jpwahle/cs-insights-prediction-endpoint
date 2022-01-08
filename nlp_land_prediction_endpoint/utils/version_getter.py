"""Module for getting the version of NLP-Land-backend"""
import os

import requests
from decouple import config  # type: ignore


def get_backend_version() -> None:
    """Utility function which provides to correct version for the backend"""
    if config("AUTH_BACKEND_VERSION", default=None) is None:
        if config("AUTH_BACKEND_URL").endswith("{version}"):
            AUTH_BACKEND_VERSION_ROUTE = config("AUTH_BACKEND_URL").format(version="version")
            version_response = requests.get(AUTH_BACKEND_VERSION_ROUTE)
            version = version_response.json()
            if "__v" in version:
                AUTH_BACKEND_VERSION = "v" + str(version["__v"])
                os.environ["AUTH_BACKEND_VERSION"] = AUTH_BACKEND_VERSION
                new_backend_url = config("AUTH_BACKEND_URL").format(version=AUTH_BACKEND_VERSION)
                os.environ["AUTH_BACKEND_URL"] = new_backend_url
    else:
        new_backend_url = config("AUTH_BACKEND_URL").format(version=config("AUTH_BACKEND_VERSION"))
        os.environ["AUTH_BACKEND_URL"] = new_backend_url
