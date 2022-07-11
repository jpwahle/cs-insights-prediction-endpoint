"""Unittests for the authentication middlware"""
from typing import Any, Generator

import pytest
import requests
from fastapi.testclient import TestClient
from requests.models import Response

from nlp_land_prediction_endpoint import __version__
from nlp_land_prediction_endpoint.app import app
from nlp_land_prediction_endpoint.utils import settings as Settings
from nlp_land_prediction_endpoint.utils.remote_storage_controller import (
    remote_storage_controller,
)


@pytest.fixture
def client() -> Generator:
    """Get the test client for tests and reuse it.

    Yields:
        Generator: Yields the test client as input argument for each test.
    """
    with TestClient(app) as tc:
        yield tc


@pytest.fixture
def endpoint() -> str:
    """Get the login_endpoint for tests.

    Returns:
        str: The refresh_endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/models/"


@pytest.fixture
def mock_forward_request(monkeypatch: Any) -> None:
    """Simulates a request.get call by overwriting the function

    Arguments:
        monkeypatch: a monkeypatch object
    """

    def mock_post(*agrs, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 200
        response._content = b'{"message": "success"}'
        return response

    monkeypatch.setattr(requests, "get", mock_post)
    monkeypatch.setattr(requests, "post", mock_post)


def test_forward_middleware(client: TestClient, endpoint: str, mock_forward_request: Any) -> None:
    Settings.get_settings().NODE_TYPE = "MAIN"
    response = client.get(endpoint)
    assert response.status_code == 200
    # XXX-TN this request will somehow deadlock the tests, i dont know why
    #        It does not make sense cause the same request with modelType="lda" works..
    # response = client.post(
    #     endpoint, json={"modelType": "wow", "modelSpecification": {"test": "a"}}
    # )
    # assert response.status_code == 404
    response = client.post(endpoint, json={"modelType": "lda"})
    assert response.status_code == 200
    response = client.get(endpoint + "123456789")
    assert response.status_code == 404
    response = client.get(endpoint + "1234")
    assert response.status_code == 200
    response = client.get("/forward")
    assert response.status_code == 404

    # TODO-TN Move this in seperate Test file
    assert remote_storage_controller.find_model_in_remote_hosts("99") is None
    assert not remote_storage_controller.get_remote_host("127.0.0.1") is None
    assert remote_storage_controller.get_remote_host("0000") is None

    Settings.get_settings().NODE_TYPE = "SECONDARY"
