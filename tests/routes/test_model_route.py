import mongomock  # type: ignore
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
def client() -> TestClient:
    """Get the test client for tests and reuse it.

    Yields:
        Generator: Yields the test client as input argument for each test.
    """
    return TestClient(app)


@pytest.fixture
def endpoint() -> str:
    """Get the endpoint for tests.

    Returns:
        str: The endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/models/"


@pytest.fixture
def model_creation_request() -> ModelCreationRequest:
    """Get a correct model creation request

    Returns:
        ModelCreationRequest: An correct modelcreation request
    """
    return ModelCreationRequest(model_type="lda", model_specification={"created_by": "Test"})


# TODO-AT change accordingly to changes in route_model.py
@pytest.fixture
def model_function_request() -> ModelFunctionRequest:
    """Get a correct model deletion request

    Returns:
        ModelFunctionRequest: An correct modeldeletion request
    """
    return ModelFunctionRequest(
        model_id="1234", model_type="lda", model_specification={"created_by": "Test"}
    )


# TODO-AT change accordingly to changes in route_model.py
@pytest.fixture
def model_deletion_request() -> ModelDeletionRequest:
    """Get a correct model deletion request

    Returns:
        ModelDeletionRequest: An correct modeldeletion request
    """
    return ModelDeletionRequest(
        model_id="1234", model_type="lda", model_specification={"created_by": "Test"}
    )


# TODO-AT change accordingly to changes in route_model.py
@pytest.fixture
def model_update_request() -> ModelUpdateRequest:
    """Get a correct model deletion request

    Returns:
        ModelUpdateRequest: An correct modeldeletion request
    """
    return ModelUpdateRequest(
        model_id="1234", model_type="lda", model_specification={"created_by": "Test"}
    )


@pytest.fixture
def failing_model_creation_request() -> ModelCreationRequest:
    """Get a failing model creation request

    Returns:
        ModelCreationRequest: An correct modelcreation request
    """
    return ModelCreationRequest(
        model_type="Does not exist", model_specification={"created_by": "Test"}
    )


@pytest.fixture
def model_function_call_request() -> GenericInputModel:
    """Get a correct GenericInput model used for testing the function call endpoint

    Returns:
        GenericInputModel: A GenericModelInput with a function call and empty data
    """
    return GenericInputModel(function_call="getTopics", input_data={})


@pytest.fixture
def model_failing_function_call_request() -> GenericInputModel:
    """Get an incorrect GenericInput model used for testing the function call endpoint

    Returns:
        GenericInputModel: A GenericModelInput with a function call and empty data
    """
    return GenericInputModel(function_call="NonExistent", input_data={})


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_model_create(
    client: TestClient, endpoint: str, model_creation_request: ModelCreationRequest
) -> None:
    """Test for successfull model creation

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        model_creation_request (ModelCreationRequest): A correct ModelCreationRequest
    """
    before_response_json = client.get(endpoint).json()
    response = client.post(endpoint, json=model_creation_request.dict())
    assert response.status_code == 201
    created_model_id = response.json()["model_id"]
    assert "location" in response.headers
    assert response.headers["location"] == endpoint + created_model_id
    response2 = client.get(endpoint)
    assert response2.status_code == 200
    response2_json = response2.json()
    assert "models" in response2_json
    assert "models" in before_response_json
    # assert response2_json["models"] == before_response_json["models"] + [createdModelID]


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_model_list_function_calls(client: TestClient, endpoint: str) -> None:
    """Test for listing all functions of a model

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
    """
    models = client.get(endpoint).json()
    assert "models" in models
    test_model_id = models["models"][0]
    response = client.get(endpoint + test_model_id)
    assert response.status_code == 200
    response_json = response.json()
    assert "function_calls" in response_json
    model = get_storage_controller().get_model(test_model_id)
    assert model is not None
    assert model.function_calls
    assert len(response_json["function_calls"]) == len(model.function_calls)
    failing_response = client.get(endpoint + "thisWillNeverEverExist")
    assert failing_response.status_code == 404


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_model_list_implemented(client: TestClient, endpoint: str) -> None:
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
    client: TestClient, endpoint: str, failing_model_creation_request: ModelCreationRequest
) -> None:
    """Test for failing model creation

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        failing_model_creation_request (ModelCreationRequest): An incorrect ModelCreationRequest
    """
    response = client.post(endpoint, json=failing_model_creation_request.dict())
    assert response.status_code == 404


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_model_function(
    client: TestClient, endpoint: str, model_function_call_request: GenericInputModel
) -> None:
    """Test for successfull model update

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        model_function_call_request (GenericInputModel): A GenericInput model holding the
                                                      function call as well as no data
    """
    models = client.get(endpoint).json()
    assert "models" in models
    test_model_id = models["models"][0]
    mfr = ModelFunctionRequest(model_id=test_model_id)
    response = client.post(endpoint + str(mfr.model_id), json=model_function_call_request.dict())
    assert response.status_code == 200
    response_json = response.json()
    assert "output_data" in response_json and "getTopics" in response_json["output_data"]


def test_failing_model_function(
    client: TestClient, endpoint: str, model_failing_function_call_request: GenericInputModel
) -> None:
    failing_response = client.post(
        endpoint + "nonExistentModel", json=model_failing_function_call_request.dict()
    )
    models = client.get(endpoint).json()
    assert "models" in models
    test_model_id = models["models"][0]
    mfr = ModelFunctionRequest(model_id=test_model_id)
    assert failing_response.status_code == 404
    failing_response = client.post(
        endpoint + str(mfr.model_id), json=model_failing_function_call_request.dict()
    )
    assert failing_response.status_code == 404


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_model_delete(
    client: TestClient, endpoint: str, model_deletion_request: ModelDeletionRequest
) -> None:
    """Test for successfull model deletion

    Arguments:
        client (TestClient): The current test client
        endpoint (str): Endpoint to query
        model_deletion_request (ModelDeletionRequest): A correct ModelDeletionRequest
    """
    models = client.get(endpoint).json()
    assert "models" in models
    test_model_id = models["models"][0]
    mdr = ModelDeletionRequest(model_id=test_model_id)
    response = client.delete(endpoint + str(mdr.model_id))
    assert response.status_code == 200
    deleted_model_id = response.json()["model_id"]
    assert deleted_model_id == mdr.model_id
    failing_response = client.delete(endpoint + "thisWillNeverEverExist")
    assert failing_response.status_code == 404
