import os
from typing import Any

import pytest
import requests
from requests.models import Response

from nlp_land_prediction_endpoint.utils.version_getter import get_backend_version


@pytest.fixture
def mock_version_request(monkeypatch: Any) -> None:
    """Simulates request.get by overwriting the function

    Arguments:
        monkeypatch: a monkeypatch object
    """

    def mock_get(*args, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 200
        response._content = b'{"__v": 0}'
        return response

    monkeypatch.setattr(requests, "get", mock_get)


def test_missing_backend_version(monkeypatch: Any, mock_version_request: Any) -> None:
    envs = {
        "AUTH_BACKEND_VERSION": None,
        "AUTH_BACKEND_URL": "http://127.0.0.1/api/{version}",
        "AUTH_BACKEND_LOGIN_ROUTE": "/auth/login/service",
        "AUTH_TOKEN_ROUTE": "/auth/service",
        "JWT_SECRET": "super_secret_secret",
        "JWT_TOKEN_EXPIRATION_MINUTES": 30,
        "JWT_SIGN_ALG": "HS256",
    }
    monkeypatch.setattr(os, "environ", envs)
    get_backend_version()
