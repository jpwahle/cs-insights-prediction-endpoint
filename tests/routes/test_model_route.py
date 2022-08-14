from typing import Generator

import mongomock
import pytest
from fastapi.testclient import TestClient

from cs_insights_prediction_endpoint import __version__
from cs_insights_prediction_endpoint.app import app
from cs_insights_prediction_endpoint.models.generic_model import GenericInputModel
from cs_insights_prediction_endpoint.routes.route_model import (
    ModelCreationRequest,
    ModelDeletionRequest,
    ModelFunctionRequest,
    ModelUpdateRequest,
)
from cs_insights_prediction_endpoint.utils.storage_controller import (
    get_storage_controller,
)


@pytest.fixture()
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


# TODO-AT change accordingly to changes in route_model.py
@pytest.fixture
def modelFunctionRequest() -> ModelFunctionRequest:
    """Get a correct model deletion request

    Returns:
        ModelFunctionRequest: An correct modeldeletion request
    """
    return ModelFunctionRequest(
        modelID="1234", modelType="lda", modelSpecification={"createdBy": "Test"}
    )


# TODO-AT change accordingly to changes in route_model.py
@pytest.fixture
def modelDeletionRequest() -> ModelDeletionRequest:
    """Get a correct model deletion request

    Returns:
        ModelDeletionRequest: An correct modeldeletion request
    """
    return ModelDeletionRequest(
        modelID="1234", modelType="lda", modelSpecification={"createdBy": "Test"}
    )


# TODO-AT change accordingly to changes in route_model.py
@pytest.fixture
def modelUpdateRequest() -> ModelUpdateRequest:
    """Get a correct model deletion request

    Returns:
        ModelUpdateRequest: An correct modeldeletion request
    """
    return ModelUpdateRequest(
        modelID="1234", modelType="lda", modelSpecification={"createdBy": "Test"}
    )


@pytest.fixture
def failingModelCreationRequest() -> ModelCreationRequest:
    """Get a failing model creation request

    Returns:
        ModelCreationRequest: An correct modelcreation request
    """
    return ModelCreationRequest(
        modelType="Does not exist", modelSpecification={"createdBy": "Test"}
    )


@pytest.fixture
def modelFunctionCallRequest() -> GenericInputModel:
    """Get a correct GenericInput model used for testing the function call endpoint

    Returns:
        GenericInputModel: A GenericModelInput with a function call and empty data
    """
    return GenericInputModel(functionCall="getTopics", inputData={})


@mongomock.patch(servers=(("127.0.0.1", 27017),))
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


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_model_list_functionCalls(client: Generator, endpoint: str) -> None:
    """Test for listing all functions of a model

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
    """
    models = client.get(endpoint).json()
    assert "models" in models
    testModelID = models["models"][0]
    response = client.get(endpoint + testModelID)
    assert response.status_code == 200
    response_json = response.json()
    assert "functionCalls" in response_json
    assert len(response_json["functionCalls"]) == len(
        get_storage_controller().getModel(testModelID).functionCalls
    )
    failing_response = client.get(endpoint + "thisWillNeverEverExist")
    assert failing_response.status_code == 404


@mongomock.patch(servers=(("127.0.0.1", 27017),))
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


@mongomock.patch(servers=(("127.0.0.1", 27017),))
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


# TODO
# def test_model_update(
#     client: Generator, endpoint: str, modelUpdateRequest: ModelUpdateRequest
# ) -> None:
#     """Test for successfull model update
#
#     Arguments:
#         client (TestClient): The current test client
#         endpoint (str): Endpoint to query
#         modelUpdateRequest (ModelUpdateRequest): A correct ModelUpdateRequest
#     """
#     response = client.patch(endpoint, json=modelUpdateRequest.dict())
#     assert response.status_code == 201
#     updatedModelID = response.json()["modelID"]
#     assert updatedModelID == modelUpdateRequest.modelID
#     assert "modelID" in response.headers


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_model_function(
    client: Generator, endpoint: str, modelFunctionCallRequest: GenericInputModel
) -> None:
    """Test for successfull model update

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        modelFunctionCallRequest (GenericInputModel): A GenericInput model holding the
                                                      function call as well as no data
    """
    models = client.get(endpoint).json()
    assert "models" in models
    testModelID = models["models"][0]
    mfr = ModelFunctionRequest(modelID=testModelID)
    response = client.post(
        endpoint + str(mfr.modelID), json=modelFunctionCallRequest.dict()
    )  # TODO remove /test
    assert response.status_code == 200
    failing_response = client.post(
        endpoint + "nonExistentModel", json={"functionCall": "ThisWillNeverExists", "inputData": {}}
    )  # TODO make a proper pyfixture
    assert failing_response.status_code == 404
    failing_response = client.post(
        endpoint + str(mfr.modelID), json={"functionCall": "ThisWillNeverExists", "inputData": {}}
    )  # TODO make a proper pyfixture
    assert failing_response.status_code == 404


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_model_delete(
    client: Generator, endpoint: str, modelDeletionRequest: ModelDeletionRequest
) -> None:
    """Test for successfull model deletion

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        modelDeletionRequest (ModelDeletionRequest): A correct ModelDeletionRequest
    """
    models = client.get(endpoint).json()
    assert "models" in models
    testModelID = models["models"][0]
    mdr = ModelDeletionRequest(modelID=testModelID)
    response = client.delete(endpoint + str(mdr.modelID))
    assert response.status_code == 200
    deletedModelID = response.json()["modelID"]
    assert deletedModelID == mdr.modelID
    failing_response = client.delete(endpoint + "thisWillNeverEverExist")
    assert failing_response.status_code == 404
