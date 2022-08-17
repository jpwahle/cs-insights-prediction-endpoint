from importlib import reload
from typing import Any, Generator

import mongomock
import pytest
import requests
from fastapi.testclient import TestClient
from requests.models import Response

import cs_insights_prediction_endpoint.app as app
from cs_insights_prediction_endpoint import __version__
from cs_insights_prediction_endpoint.models.generic_model import generic_input_model
from cs_insights_prediction_endpoint.models.model_hosts import remote_host
from cs_insights_prediction_endpoint.routes.route_model import (
    model_creation_request,
    model_deletion_request,
    model_function_request,
)
from cs_insights_prediction_endpoint.utils.settings import get_settings


@pytest.fixture
def patch_settings(monkeypatch: Any) -> None:
    monkeypatch.setattr(get_settings(), "node_type", "MAIN")


@pytest.fixture
def client(patch_settings: Any) -> Generator:
    """Get the test client for tests and reuse it.

    Yields:
        Generator: Yields the test client as input argument for each test.
    """
    reload_app = reload(app)
    with TestClient(reload_app.app) as tc:
        yield tc


@pytest.fixture
def endpoint() -> str:
    """Get the endpoint for tests.

    Returns:
        str: The endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/models/"


@pytest.fixture
def mock_deletion(monkeypatch: Any) -> None:
    def mock_post(*args, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 200
        response._content = b'{"model_id": "1234"}'
        return response

    monkeypatch.setattr(requests, "delete", mock_post)


@pytest.fixture
def hosts_endpoint() -> str:
    """Get the endpoint for tests.

    Returns:
        str: The endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/hosts/"


@pytest.fixture
def dummy_remote_host() -> remote_host:
    dummy_remote_host = {
        "ip": "192.168.0.100",
        "port": "666",
        "models": ["lda"],
        "created_models": ["1234"],
    }
    return remote_host(**dummy_remote_host)


@pytest.fixture
def remote_host_creation(
    client: TestClient, dummy_remote_host: remote_host, hosts_endpoint: str
) -> None:
    """Creates a dummy remote Host for further tests"""
    client.post(hosts_endpoint, json=dummy_remote_host.dict())


@pytest.fixture
def mock_post_request(monkeypatch: Any) -> None:
    def mock_post(*args, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 200
        response._content = b"{}"
        return response

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_get_request(monkeypatch: Any) -> None:
    def mock_get(*args, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 200
        response._content = b'{"models": []"}'
        return response

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_creation(monkeypatch: Any) -> None:
    def mock_post(*args, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 201
        response._content = b'{"model_id": "1234"}'
        return response

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def failing_model_creation_request() -> model_creation_request:
    """Get a correct model creation request

    Returns:
        model_creation_request: An correct modelcreation request
    """
    return model_creation_request(
        model_type="non Existent", modelSpecification={"created_by": "Test"}
    )


@pytest.fixture
def model_creation_request() -> model_creation_request:
    """Get a correct model creation request

    Returns:
        model_creation_request: An correct modelcreation request
    """
    return model_creation_request(model_type="lda", modelSpecification={"created_by": "Test"})


@pytest.fixture
def model_function_request() -> model_function_request:
    """Get a correct model deletion request

    Returns:
        model_function_request: An correct modeldeletion request
    """
    return model_function_request(
        model_id="1234", model_type="lda", modelSpecification={"created_by": "Test"}
    )


# TODO-AT change accordingly to changes in route_model.py
@pytest.fixture
def model_deletion_request() -> model_deletion_request:
    """Get a correct model deletion request

    Returns:
        model_deletion_request: An correct modeldeletion request
    """
    return model_deletion_request(
        model_id="1234", model_type="lda", modelSpecification={"created_by": "Test"}
    )


@pytest.fixture
def model_function_call_request() -> generic_input_model:
    dummy_input = {"input_data": {}, "function_call": "test"}
    return generic_input_model(**dummy_input)


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_all_gets_forward(
    client: TestClient,
    endpoint: str,
    mock_get_request: Any,
    remote_host_creation: Any,
    dummy_remote_host: remote_host,
) -> None:
    response = client.get(endpoint)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["models"] == dummy_remote_host.created_models
    response = client.get(endpoint + "implemented")
    assert response.status_code == 200
    response_json = response.json()
    assert "models" in response_json
    assert response_json["models"] == dummy_remote_host.models
    response = client.get(endpoint + "1234")
    assert response.status_code == 200


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_add_model_forward(
    client: TestClient,
    endpoint: str,
    model_creation_request: model_creation_request,
    failing_model_creation_request: model_creation_request,
    mock_creation: Any,
) -> None:
    response = client.post(endpoint, json=model_creation_request.dict())
    assert response.status_code == 201
    response = client.post(endpoint, json=failing_model_creation_request.dict())
    assert response.status_code == 404


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_function_call_model_forward(
    client: TestClient,
    endpoint: str,
    model_function_call_request: generic_input_model,
    mock_post_request: Any,
) -> None:
    response = client.post(endpoint + "1234", json=model_function_call_request.dict())
    assert response.status_code == 200


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_delete_model_forward(client: TestClient, endpoint: str, mock_deletion: Any) -> None:
    response = client.delete(endpoint + "1234")
    assert response.status_code == 200
    response_json = response.json()
    assert "model_id" in response_json
    assert response_json["model_id"] == "1234"
