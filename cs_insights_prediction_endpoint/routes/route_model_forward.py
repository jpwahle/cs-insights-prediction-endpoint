"""This module implements the endpoint logic for models."""
from typing import List, Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from cs_insights_prediction_endpoint import __version__
from cs_insights_prediction_endpoint.models.generic_model import generic_input_model
from cs_insights_prediction_endpoint.utils.remote_storage_controller import (
    get_remote_storage_controller,
    remote_storage_controller,
)

# from cs_insights_prediction_endpoint.models.lda_model import LDAModel
from cs_insights_prediction_endpoint.utils.settings import Settings, get_settings
from cs_insights_prediction_endpoint.utils.storage_controller import (
    get_storage_controller,
    storage_controller,
)

router: APIRouter = APIRouter()


class storage_controller_list_reponse(BaseModel):
    """Response model for both
        - GET /
        - GET /implemented
    which returns a list of models
    """

    models: List[str]


class model_creation_request(BaseModel):
    """Response model for creating a Model
    This contains the model_type (e.g., lda) and the model specification
    which should be parsable to the model_types pydentic schema.
    """

    model_type: str
    model_specification: dict


@router.get(
    "/implemented",
    response_description="Lists all currently available(implemented) models",
    response_model=storage_controller_list_reponse,
    status_code=status.HTTP_200_OK,
)
def forward_list_all_implemented_models(
    settings: Settings = Depends(get_settings),
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> storage_controller_list_reponse:
    """Endpoint for getting a list of all implemented models"""
    return storage_controller_list_reponse(models=rsc.get_all_models())


@router.get(
    "/{current_model_id}",
    response_description="Lists all function calls of the current model",
    # response_model=ModelSpecificFunctionCallResponse,
    status_code=status.HTTP_200_OK,
)
def forward_list_all_function_calls(
    request: Request,
    current_model_id: str,
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> Response:
    """Endpoint for getting a list of all implemented function calls"""
    host = get_host(current_model_id, rsc)
    r = requests.get(f"http://{host}{request.url.path}")
    return build_response(r)


@router.delete(
    "/{current_model_id}",
    response_description="Delete the current model",
    # response_model=ModelDeletionResponse,
    status_code=status.HTTP_200_OK,
)
def forward_deleteModel(
    request: Request,
    current_model_id: str,
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> Response:
    """Endpoint for deleting a model"""
    host = get_host(current_model_id, rsc)
    r = requests.delete(f"http://{host}{request.url.path}")
    if host is not None and r.ok:
        rsc.remove_model_from_created_model_list(host.split(":")[0], current_model_id)
    return build_response(r)


@router.get(
    "/",
    response_description="Lists all currently created models",
    # response_model=storage_controller_list_reponse,
    status_code=status.HTTP_200_OK,
)
def forward_list_all_created_models(
    settings: Settings = Depends(get_settings),
    sc: storage_controller = Depends(get_storage_controller),
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> storage_controller_list_reponse:
    """Endpoint for getting a list of all created models"""
    all_models = rsc.get_all_created_models()
    return storage_controller_list_reponse(models=all_models)


@router.post(
    "/",
    response_description="Creates a model",
    # response_model=ModelCreationResponse,
    status_code=status.HTTP_201_CREATED,
)
def forward_create_model(
    request: Request,
    model_creation_request: model_creation_request,
    settings: Settings = Depends(get_settings),
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> Response:
    """Endpoint for creating a model

    Arguments:
        model_creation_request (model_creation_request): A model_creation_request used for the
        creation of the actual model

    Returns:
        dict: Either an error or the created model id
    """
    host = rsc.find_model_in_remote_hosts(model_creation_request.model_type)
    if host is None:
        raise HTTPException(status_code=404, detail="No hosts contain the specified model")
    else:
        r = requests.post(f"http://{host}{request.url.path}", json=model_creation_request.dict())
        response = build_response(r)
        if r.ok:
            # Append new model to list:
            model_id = r.json()["model_id"]
            rsc.add_model_to_created_model_list(host.split(":")[0], model_id)
            response.headers["location"] = f"/api/v{__version__.split('.')[0]}/models/{model_id}"
        return response


@router.post(
    "/{current_model_id}",
    response_description="Runs a function",
    # response_model=generic_output_model,
    status_code=status.HTTP_200_OK,
)
def forward_getInformation(
    request: Request,
    current_model_id: str,
    generic_input: generic_input_model,
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> Response:
    """Gets info out of post data"""
    host = get_host(current_model_id, rsc)
    r = requests.post(f"http://{host}{request.url.path}", json=generic_input.dict())
    return build_response(r)


def get_host(current_model_id: str, rsc: remote_storage_controller) -> Optional[str]:
    """Get host containing the model current_model_id"""
    return rsc.find_created_model_in_remote_hosts(current_model_id)


def build_response(r: requests.Response) -> Response:
    """Build the Response from a requests.Response object"""
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type="application/json",
    )
