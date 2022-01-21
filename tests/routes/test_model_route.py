from typing import Generator

import pytest
from fastapi.testclient import TestClient

from nlp_land_prediction_endpoint import __version__
from nlp_land_prediction_endpoint.app import app
from nlp_land_prediction_endpoint.routes.route_model import ModelCreationRequest


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
    return f"/api/v{__version__.split('.')[0]}/models/"


@pytest.fixture
def modelCreationRequest() -> ModelCreationRequest:
    """Get a correct model creation request

    Returns:
        ModelCreationRequest: An correct modelcreation request
    """
    return ModelCreationRequest(modelType="lda", modelSpecification={"createdBy": "Test"})


@pytest.fixture
def failingModelCreationRequest() -> ModelCreationRequest:
    """Get a failing model creation request

    Returns:
        ModelCreationRequest: An correct modelcreation request
    """
    return ModelCreationRequest(
        modelType="Does not exist", modelSpecification={"createdBy": "Test"}
    )


def test_model_create(
    client: Generator, endpoint: str, modelCreationRequest: ModelCreationRequest
) -> None:
    """Test for successfull model creation

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        modelCreationRequest (ModelCreationRequest): A correct ModelCreationRequest
    """
    response = client.post(endpoint, json=modelCreationRequest.dict())
    assert response.status_code == 201
    createdModelID = response.json()["modelID"]
    assert "location" in response.headers
    assert response.headers["location"] == endpoint + createdModelID
    response2 = client.get(endpoint)
    assert response2.status_code == 200
    response2_json = response2.json()
    assert "models" in response2_json
    assert response2_json["models"] == [createdModelID]


def test_model_list_implemented(client: Generator, endpoint: str) -> None:
    """Test for listing implemented models

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
    """
    response = client.get(endpoint + "implemented")
    assert response.status_code == 200
    response_json = response.json()
    assert "models" in response_json
    assert "lda" in response_json["models"]


def test_model_create_fail(
    client: Generator, endpoint: str, failingModelCreationRequest: ModelCreationRequest
) -> None:
    """Test for failing model creation

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        failingModelCreationRequest (ModelCreationRequest): An incorrect ModelCreationRequest
    """
    response = client.post(endpoint, json=failingModelCreationRequest.dict())
    assert response.status_code == 404
