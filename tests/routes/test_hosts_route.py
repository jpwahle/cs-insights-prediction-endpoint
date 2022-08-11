from typing import Generator

import pytest
from fastapi.testclient import TestClient

from nlp_land_prediction_endpoint import __version__
from nlp_land_prediction_endpoint.app import app
from nlp_land_prediction_endpoint.models.model_hosts import RemoteHost
from nlp_land_prediction_endpoint.routes.route_hosts import RemoteHostDeleteRequest


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
    """Get the endpoint for tests.

    Returns:
        str: The endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/hosts/"


@pytest.fixture
def remote_host_creation_request() -> RemoteHost:
    """Get a correct model creation request

    Returns:
        ModelCreationRequest: An correct modelcreation request
    """
    dummy_remote_host = {
        "ip": "192.168.0.100",
        "port": "666",
        "models": ["test"],
        "created_models": [],
    }
    return RemoteHost(**dummy_remote_host)


@pytest.fixture
def remote_host_deletion_request() -> RemoteHostDeleteRequest:
    """Get a correct model deletion request

    Returns:
        ModelCreationRequest: An correct model deletion request
    """
    return RemoteHostDeleteRequest(ip="192.168.0.100")


@pytest.fixture
def failing_remote_host_deletion_request() -> RemoteHostDeleteRequest:
    """Get a correct model deletion request

    Returns:
        ModelCreationRequest: An correct model deletion request
    """
    return RemoteHostDeleteRequest(ip="this.is.not.a.vaild.ip.....")


def test_remote_hosts_add(
    client: TestClient, endpoint: str, remote_host_creation_request: RemoteHost
) -> None:
    remote_host_list = client.get(endpoint).json()
    response = client.post(endpoint, json=remote_host_creation_request.dict())
    assert response.status_code == 200
    assert remote_host_list != client.get(endpoint).json()


def test_remote_hosts_delete(
    client: TestClient, endpoint: str, remote_host_deletion_request: RemoteHostDeleteRequest
) -> None:
    response = client.delete(endpoint, json=remote_host_deletion_request.dict())
    assert response.status_code == 200
    assert response.json()["ip"] == remote_host_deletion_request.ip


def test_remote_hosts_delete_fail(
    client: TestClient, endpoint: str, failing_remote_host_deletion_request: RemoteHostDeleteRequest
) -> None:
    response = client.delete(endpoint, json=failing_remote_host_deletion_request.dict())
    assert response.status_code == 404
