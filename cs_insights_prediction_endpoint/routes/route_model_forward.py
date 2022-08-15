"""This module implements the endpoint logic for models."""
from typing import List, Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from cs_insights_prediction_endpoint import __version__
from cs_insights_prediction_endpoint.models.generic_model import GenericInputModel
from cs_insights_prediction_endpoint.utils.remote_storage_controller import (
    RemoteStorageController,
    get_remote_storage_controller,
)

# from cs_insights_prediction_endpoint.models.lda_model import LDAModel
from cs_insights_prediction_endpoint.utils.settings import Settings, get_settings
from cs_insights_prediction_endpoint.utils.storage_controller import (
    StorageController,
    get_storage_controller,
)

router: APIRouter = APIRouter()


class StorageControllerListReponse(BaseModel):
    """Response model for both
        - GET /
        - GET /implemented
    which returns a list of models
    """

    models: List[str]


class ModelCreationRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    modelType: str
    modelSpecification: dict


@router.get(
    "/implemented",
    response_description="Lists all currently available(implemented) models",
    response_model=StorageControllerListReponse,
    status_code=status.HTTP_200_OK,
)
def forward_list_all_implemented_models(
    settings: Settings = Depends(get_settings),
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> StorageControllerListReponse:
    """Endpoint for getting a list of all implemented models"""
    return StorageControllerListReponse(models=rsc.get_all_models())


@router.get(
    "/{current_modelID}",
    response_description="Lists all function calls of the current model",
    # response_model=ModelSpecificFunctionCallResponse,
    status_code=status.HTTP_200_OK,
)
def forward_list_all_function_calls(
    request: Request,
    current_modelID: str,
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> Response:
    """Endpoint for getting a list of all implemented function calls"""
    host = get_host(current_modelID, rsc)
    r = requests.get(f"http://{host}{request.url.path}")
    return build_response(r)


@router.delete(
    "/{current_modelID}",
    response_description="Delete the current model",
    # response_model=ModelDeletionResponse,
    status_code=status.HTTP_200_OK,
)
def forward_deleteModel(
    request: Request,
    current_modelID: str,
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> Response:
    """Endpoint for deleting a model"""
    host = get_host(current_modelID, rsc)
    r = requests.delete(f"http://{host}{request.url.path}")
    if host is not None and r.ok:
        rsc.remove_model_from_created_model_list(host.split(":")[0], current_modelID)
    return build_response(r)


@router.get(
    "/",
    response_description="Lists all currently created models",
    # response_model=StorageControllerListReponse,
    status_code=status.HTTP_200_OK,
)
def forward_list_all_created_models(
    settings: Settings = Depends(get_settings),
    sc: StorageController = Depends(get_storage_controller),
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> StorageControllerListReponse:
    """Endpoint for getting a list of all created models"""
    all_models = rsc.get_all_created_models()
    return StorageControllerListReponse(models=all_models)


@router.post(
    "/",
    response_description="Creates a model",
    # response_model=ModelCreationResponse,
    status_code=status.HTTP_201_CREATED,
)
def forward_create_model(
    request: Request,
    modelCreationRequest: ModelCreationRequest,
    settings: Settings = Depends(get_settings),
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> Response:
    """Endpoint for creating a model

    Arguments:
        modelCreationRequest (ModelCreationRequest): A ModelCreationRequest used for the creation
                                                 of the actual model

    Returns:
        dict: Either an error or the created model id
    """
    host = rsc.find_model_in_remote_hosts(modelCreationRequest.modelType)
    if host is None:
        raise HTTPException(status_code=404, detail="No hosts contain the specified model")
    else:
        r = requests.post(f"http://{host}{request.url.path}", json=modelCreationRequest.dict())
        response = build_response(r)
        if r.ok:
            # Append new model to list:
            model_id = r.json()["modelID"]
            rsc.add_model_to_created_model_list(host.split(":")[0], model_id)
            response.headers["location"] = f"/api/v{__version__.split('.')[0]}/models/{model_id}"
        return response


@router.post(
    "/{current_modelID}",
    response_description="Runs a function",
    # response_model=GenericOutputModel,
    status_code=status.HTTP_200_OK,
)
def forward_getInformation(
    request: Request,
    current_modelID: str,
    genericInput: GenericInputModel,
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> Response:
    """Gets info out of post data"""
    host = get_host(current_modelID, rsc)
    r = requests.post(f"http://{host}{request.url.path}", json=genericInput.dict())
    return build_response(r)


def get_host(current_modelID: str, rsc: RemoteStorageController) -> Optional[str]:
    """Get host containing the model current_modelID"""
    return rsc.find_created_model_in_remote_hosts(current_modelID)


def build_response(r: requests.Response) -> Response:
    """Build the Response from a requests.Response object"""
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type="application/json",
    )
