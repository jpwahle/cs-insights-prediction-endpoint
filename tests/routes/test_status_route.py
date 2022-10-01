"""Test the status route."""
import pytest
from fastapi.testclient import TestClient

from cs_insights_prediction_endpoint import __version__
from cs_insights_prediction_endpoint.app import app


@pytest.fixture
def client() -> TestClient:
    """Get the test client for tests and reuse it.

    Yields:
        TestClient: Yields the test client as input argument for each test.
    """
    with TestClient(app) as client:
        return client


@pytest.fixture
def endpoint() -> str:
    """Get the endpoint for tests.

    Returns:
        str: The endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/status"


def test_backend_status(client: TestClient, endpoint: str) -> None:
    """Test the backend status.

    Args:
        client (TestClient): The current test client.
        endpoint (str): Endpoint prefix.
    """
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "version": __version__}
