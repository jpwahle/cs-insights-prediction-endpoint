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


# TODO New tests for new routes:
# Model
#   delete

def test_model_delete(
    client: Generator, endpoint: str, modelDeletionRequest: ModelDeletionRequest
) -> None:
    """Test for successfull model deletion

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        modelDeletionRequest (ModelDeletionRequest): A correct ModelDeletionRequest
    """
    response = client.delete(endpoint, json=modelDeletionRequest.dict())
    assert response.status_code == 200
    createdModelID = response.json()["data"]
    assert "done" in response.headers


#   update

def test_model_update(
    client: Generator, endpoint: str, modelUpdateRequest: ModelUpdateRequest
) -> None:
    """Test for successfull model update

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        modelUpdateRequest (ModelUpdateRequest): A correct ModelUpdateRequest
    """
    response = client.patch(endpoint, json=modelUpdateRequest.dict())
    assert response.status_code == 201
    createdModelID = response.json()["modelID"]
    assert "modelID" in response.headers


# Model/function/args
#   post

def test_model_function(
    client: Generator, endpoint: str, modelFunctionRequest: ModelFunctionRequest
) -> None:
    """Test for successfull model update

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        modelFunctionRequest (ModelFunctionRequest): A correct ModelFunctionRequest
    """
    response = client.post(endpoint, json=modelFunctionRequest.dict())
    assert response.status_code == 200
    createdModelID = response.json()["output_model"]
    assert "output_model" in response.headers