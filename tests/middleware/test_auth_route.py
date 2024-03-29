"""Unittests for the authentication middlware"""
import os
import time
from datetime import datetime
from typing import Any

import pytest
import requests
from fastapi.testclient import TestClient
from requests.models import Response

from cs_insights_prediction_endpoint import __version__
from cs_insights_prediction_endpoint.app import app
from cs_insights_prediction_endpoint.middleware.auth import create_token, decode_token
from cs_insights_prediction_endpoint.models.model_token import TokenModel
from cs_insights_prediction_endpoint.models.model_token_data import TokenData
from cs_insights_prediction_endpoint.models.model_user import UserModel
from cs_insights_prediction_endpoint.models.model_user_login import UserLoginModel
from cs_insights_prediction_endpoint.utils.settings import get_settings


@pytest.fixture
def client() -> TestClient:
    """Get the test client for tests and reuse it.

    Yields:
        TestClient: Yields the test client as input argument for each test.
    """
    with TestClient(app) as client:
        return client


@pytest.fixture
def refresh_endpoint() -> str:
    """Get the login_endpoint for tests.

    Returns:
        str: The refresh_endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/auth/refresh"


@pytest.fixture
def login_endpoint() -> str:
    """Get the login_endpoint for tests.

    Returns:
        str: The login_endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/auth/login"


@pytest.fixture
def dummy_login() -> UserLoginModel:
    """Create a dummy login.

    Returns:
        UserLoginModel: an example UserLoginModel
    """
    example = UserLoginModel.Config.schema_extra.get("example")
    assert example
    return UserLoginModel(**example)


@pytest.fixture
def dummy_user() -> UserModel:
    """Create a dummy user.

    Returns:
        UserModel: an example UserModel
    """
    example = UserModel.Config.schema_extra.get("example")
    assert example
    return UserModel(**example)


@pytest.fixture
def dummy_token() -> str:
    """Create a dummy token.

    Returns:
        str: a valid token created from example in UserModel
    """
    example = UserModel.Config.schema_extra.get("example")
    assert example
    user = TokenData(**example)
    token = create_token(user, get_settings())
    return token


@pytest.fixture
def mock_post(monkeypatch: Any) -> None:
    """Simulates a request.post call by overwriting the function

    Arguments:
        monkeypatch: a monkeypatch object
    """

    def mock_post(*agrs, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 200
        response._content = b'{"email": "test@test.de"}'
        return response

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_post_failure(monkeypatch: Any) -> None:
    """Simulates a request.post call by overwriting the function

    Arguments:
        monkeypatch: a monkeypatch object
    """

    def mock_post(*agrs, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 401
        response._content = b'{"message": "error"}'
        return response

    monkeypatch.setattr(requests, "post", mock_post)


def test_simulated_existing_failed_auth(
    client: TestClient,
    login_endpoint: str,
    dummy_login: UserLoginModel,
    mock_post_failure: Any,
) -> None:
    """Test the login endpoint with a failed authentication attempt

    Arguments:
        client (TestClient): The current test client.
        login_endpoint (str): Endpoint prefix.
        dummy_login (UserLoginModel): A dummy user to test.
        mock_post_failure (Any): this overwrites the request.post call
    """
    os.environ["AUTH_BACKEND_URL"] = "http://127.0.0.1"
    os.environ["AUTH_TOKEN_ROUTE"] = login_endpoint
    response = client.post(login_endpoint, json=dummy_login.dict())
    assert response.status_code == 401


def test_simulated_existing_auth_success(
    client: TestClient,
    login_endpoint: str,
    dummy_login: UserLoginModel,
    mock_post: Any,
) -> None:
    """Test the login endpoint with a successful authentication attempt

    Arguments:
        client (TestClient): The current test client.
        login_endpoint (str): Endpoint prefix.
        dummy_login (UserLoginModel): A dummy user to test.
        mock_post (Any): this overwrites the request.post call
    """
    os.environ["AUTH_BACKEND_URL"] = "http://127.0.0.1"
    os.environ["AUTH_TOKEN_ROUTE"] = login_endpoint
    response = client.post(login_endpoint, json=dummy_login.dict())
    assert response.status_code == 200
    token = TokenModel(**response.json())
    decoded_token = decode_token(token.access_token, get_settings())
    assert decoded_token is not None


def test_non_existing_auth(
    client: TestClient, login_endpoint: str, dummy_login: UserLoginModel
) -> None:
    """Test the login endpoint with a non existing host and endpoint

    Arguments:
        client (TestClient): The current test client.
        login_endpoint (str): Endpoint prefix.
        dummy_login (UserLoginModel): A dummy user to test.
    """
    os.environ["AUTH_BACKEND_URL"] = "http://127.0.0.1"
    os.environ["AUTH_TOKEN_ROUTE"] = login_endpoint
    response = client.post(login_endpoint, json=dummy_login.dict())
    assert response.status_code == 401


def test_refresh_forged(client: TestClient, refresh_endpoint: str) -> None:
    """Test the refresh endpoint with a invalid token

    Arguments:
        client (TestClient): The current test client.
        refresh_endpoint (str): Endpoint prefix.
    """
    response = client.post(refresh_endpoint, headers={"Authorization": "Bearer 123"})
    assert response.status_code == 401


def test_refresh(client: TestClient, refresh_endpoint: str, dummy_token: str) -> None:
    """Test the refresh endpoint with a valid token

    Arguments:
        client (TestClient): The current test client.
        refresh_endpoint (str): Endpoint prefix.
        dummy_token (str): a valid dummy token
    """
    time.sleep(1)
    response = client.post(refresh_endpoint, headers={"Authorization": f"Bearer {dummy_token}"})
    assert response.status_code == 200
    refresh_token = TokenModel(**response.json())
    decoded_refresh = decode_token(refresh_token.access_token, get_settings())
    decoded_dummy = decode_token(dummy_token, get_settings())
    assert decoded_refresh.exp
    assert decoded_dummy.exp
    assert datetime.fromtimestamp(int(decoded_refresh.exp)) > datetime.fromtimestamp(
        int(decoded_dummy.exp)
    )
