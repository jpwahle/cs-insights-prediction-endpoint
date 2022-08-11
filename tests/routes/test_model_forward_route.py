from typing import Any

import pytest
import requests
from fastapi.testclient import TestClient
from requests.models import Response

from nlp_land_prediction_endpoint import __version__
from nlp_land_prediction_endpoint.app import app
from nlp_land_prediction_endpoint.routes.route_model import (
    ModelCreationRequest,
    ModelDeletionRequest,
    ModelFunctionRequest,
)
from nlp_land_prediction_endpoint.utils.settings import get_settings


@pytest.fixture
def endpoint() -> str:
    """Get the endpoint for tests.

    Returns:
        str: The endpoint including current version.
    """
    return f"/api/v{__version__.split('.')[0]}/models/"


@pytest.fixture
def patch_settings(monkeypatch: Any) -> None:
    monkeypatch.setattr(get_settings(), "NODE_TYPE", "MAIN")
    # monkeypatch.setenv("NODE_TYPE", "MAIN")


@pytest.fixture
def mock_deletion(monkeypatch: Any) -> None:
    def mock_post(*args, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 200
        response._content = b'{"modelID": "1234"}'
        return response

    monkeypatch.setattr(requests, "delete", mock_post)


@pytest.fixture
def mock_creation(monkeypatch: Any) -> None:
    def mock_post(*args, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 201
        response._content = b'{"modelID": "1234"}'
        return response

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def modelCreationRequest() -> ModelCreationRequest:
    """Get a correct model creation request

    Returns:
        ModelCreationRequest: An correct modelcreation request
    """
    return ModelCreationRequest(modelType="lda", modelSpecification={"createdBy": "Test"})


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


def test_list_implemented(
    endpoint: str,
    patch_settings: Any,
) -> None:
    get_settings().NODE_TYPE = "MAIN"
    with TestClient(app) as client:
        response = client.get(endpoint + "implemented")
        assert response.status_code == 200


def test_add_model(
    endpoint: str,
    modelCreationRequest: ModelCreationRequest,
    patch_settings: Any,
    mock_creation: Any,
) -> None:
    get_settings().NODE_TYPE = "MAIN"
    with TestClient(app) as client:
        response = client.post(endpoint, json=modelCreationRequest.dict())
        assert response.status_code == 201


def test_delete_model(endpoint: str, patch_settings: Any, mock_deletion: Any) -> None:
    get_settings().NODE_TYPE = "MAIN"
    with TestClient(app) as client:
        response = client.delete(endpoint + "1234")
        assert response.status_code == 404
