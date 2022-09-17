"""This module implements the endpoint logic for models."""
from importlib import import_module
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel

from cs_insights_prediction_endpoint import __version__
from cs_insights_prediction_endpoint.models.generic_model import (
    GenericInputModel,
    GenericOutputModel,
)
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


class ModelSpecificFunctionCallResponse(BaseModel):
    """Response model for model specific function calls"""

    function_calls: List[str]


class ModelCreationResponse(BaseModel):
    """Response Model for the successfull creation of a model"""

    model_id: str


class ModelDeletionResponse(BaseModel):
    """Response Model for the successfull deletion of a model"""

    model_id: str


# TODO-AT TN: I just copied the ModelCreationRequest,
#         since this class was used but i could not find it
#         please change
class ModelDeletionRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    model_id: str


# TODO-AT TN: I just copied the ModelCreationRequest,
#         since this class was used but i could not find it
#         please change
class ModelFunctionRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    model_id: str


# TODO-AT TN: I just copied the ModelCreationRequest,
#         since this class was used but i could not find it
#         please change
class ModelUpdateRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    model_id: str
    model_specification: dict


class ModelCreationRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    # XXX-TN I puropsefully chose modelSpecification to be a dict since
    #          using the generic model, would incur the loss of pydantics strengths
    model_type: str
    # XXX-TN For the docker ochestration it will be helpfull to also have an input for
    #        the location of Model initialization (local, local[dockerfile], remote)
    model_specification: dict


@router.get(
    "/implemented",
    response_description="Lists all currently available(implemented) models",
    response_model=StorageControllerListReponse,
    status_code=status.HTTP_200_OK,
)
def list_all_implemented_models(
    settings: Settings = Depends(get_settings),
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> StorageControllerListReponse:
    """Endpoint for getting a list of all implemented models"""
    models = []
    for implemented_models in settings.implemented_models:
        for implemented_model in implemented_models.keys():
            models.append(implemented_model)
    return StorageControllerListReponse(models=models)


@router.get(
    "/{current_model_id}",
    response_description="Lists all function calls of the current model",
    response_model=ModelSpecificFunctionCallResponse,
    status_code=status.HTTP_200_OK,
)
def list_all_function_calls(
    current_model_id: str, sc: StorageController = Depends(get_storage_controller)
) -> BaseModel:
    """Endpoint for getting a list of all implemented function calls"""
    # validate id
    current_model = sc.get_model(current_model_id)
    if current_model is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not found")

    # get fun calls
    current_model_function_calls = (
        current_model.get_function_calls()
    )  # current model functioncalls list
    return ModelSpecificFunctionCallResponse(function_calls=current_model_function_calls)


@router.delete(
    "/{current_model_id}",
    response_description="Delete the current model",
    response_model=ModelDeletionResponse,
    status_code=status.HTTP_200_OK,
)
def delete_model(
    current_model_id: str, sc: StorageController = Depends(get_storage_controller)
) -> ModelDeletionResponse:
    """Endpoint for deleting a model"""
    # validate id
    current_model = sc.get_model(current_model_id)
    if current_model is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not implemented")

    # delete it
    sc.del_model(current_model.get_id())
    return ModelDeletionResponse(model_id=current_model_id)


@router.get(
    "/",
    response_description="Lists all currently created models",
    response_model=StorageControllerListReponse,
    status_code=status.HTTP_200_OK,
)
def list_all_created_models(
    settings: Settings = Depends(get_settings),
    sc: StorageController = Depends(get_storage_controller),
) -> StorageControllerListReponse:
    """Endpoint for getting a list of all created models"""
    all_models = list([str(i) for i in sc.get_all_models()])
    return StorageControllerListReponse(models=all_models)


@router.post(
    "/",
    response_description="Creates a model",
    response_model=ModelCreationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_model(
    model_creation_request: ModelCreationRequest,
    response: Response,
    settings: Settings = Depends(get_settings),
    sc: StorageController = Depends(get_storage_controller),
) -> ModelCreationResponse:
    """Endpoint for creating a model

    Arguments:
        modelCreationRequest (ModelCreationRequest): A ModelCreationRequest used for the creation
                                                 of the actual model

    Returns:
        dict: Either an error or the created model id
    """
    model = None
    for implemented_models in settings.implemented_models:
        if model_creation_request.model_type in implemented_models:
            model_specs = implemented_models[model_creation_request.model_type]
            model_module = import_module(model_specs[0])  # TODO Use proper model
            model_class = model_specs[1]
            model = getattr(model_module, model_class)(
                type_of_model=model_creation_request.model_type,
                **(model_creation_request.model_specification),
            )
    if model is None:
        raise HTTPException(status_code=404, detail="Model not implemented")
    sc.add_model(model)
    response.headers["location"] = f"/api/v{__version__.split('.')[0]}/models/{model.id}"

    return ModelCreationResponse(model_id=model.id)


@router.post(
    "/{current_model_id}",
    response_description="Runs a function",
    response_model=GenericOutputModel,
    status_code=status.HTTP_200_OK,
)
def get_information(
    current_model_id: str,
    generic_input: GenericInputModel,
    sc: StorageController = Depends(get_storage_controller),
) -> BaseModel:
    """Gets info out of post data"""
    return run_function(current_model_id, generic_input.function_call, generic_input.input_data, sc)


def run_function(
    current_model_id: str, req_function: str, data_input: Dict[Any, Any], sc: StorageController
) -> BaseModel:
    """Runs a given function of a given model"""
    # Validate id
    current_model = sc.get_model(current_model_id)
    if current_model is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not found")

    # Check if the function is actually availabe in the requested model
    # Return an HTTPException if not; Execute the function and return Dict otherwise
    try:
        my_fn = current_model.function_calls[req_function]
    except AttributeError:
        raise HTTPException(status_code=404, detail="Function not implemented")
    
    # Run function and parse output dict into actual response model
    output = my_fn(**data_input)
    # XXX-TN we have to ensure that we return a dict on a function call
    #        i dont know if the following is the best way to achive this
    if not type(output) is dict:
        # raise HTTPException(status_code=500, detail="Model did not return a valid response")
        output = {req_function: str(output)}  # TODO-TN this is relly hacky
    out_model_response = GenericOutputModel(output_data=output)

    return out_model_response
