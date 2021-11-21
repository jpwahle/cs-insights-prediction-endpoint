"""Test the status route."""
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from nlp_land_prediction_endpoint import __version__
from nlp_land_prediction_endpoint.app import app
from nlp_land_prediction_endpoint.models.model_paper import PaperModel


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
    return f"/api/v{__version__.split('.')[0]}/topics/"


@pytest.fixture
def dummy_paper() -> PaperModel:
    """Create a dummy paper.

    Returns:
        str: The endpoint including current version.
    """
    example = PaperModel.Config.schema_extra.get("example", {})
    return PaperModel(**example)


def test_post_topic_for_papers(client: TestClient, endpoint: str, dummy_paper: PaperModel) -> None:
    """Test the backend status.

    Args:
        client (TestClient): The current test client.
        endpoint (str): Endpoint prefix.
        dummy_paper (PaperModel): A dummy paper to test.
    """
    response = client.post(endpoint, json=dummy_paper.dict())
    assert response.status_code == 200
    assert response.json() == {
        "topics": [
            {
                "id": "5136bc054aed4daf9e2a1237",
                "name": "Topic 1",
                "score": 0.5,
                "keywords": ["keyword 1", "keyword 2"],
                "paper_ids": ["5136bc054aed4daf9e2a1239", "5136bc054aed4daf9e2a1238"],
            }
        ]
    }
