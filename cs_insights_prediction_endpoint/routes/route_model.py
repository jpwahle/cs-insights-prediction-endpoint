"""This module implements the endpoint logic for models."""
from importlib import import_module
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel

from cs_insights_prediction_endpoint import __version__
from cs_insights_prediction_endpoint.models.generic_model import (
    generic_input_model,
    generic_output_model,
)
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
    # error: str


class model_specific_function_call_response(BaseModel):
    """Response model for model specific function calls"""

    function_calls: List[str]


class model_creation_response(BaseModel):
    """Response Model for the successfull creation of a model"""

    model_id: str


class model_deletion_response(BaseModel):
    """Response Model for the successfull deletion of a model"""

    model_id: str


# TODO-AT TN: I just copied the model_creation_request,
#         since this class was used but i could not find it
#         please change
class model_deletion_request(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    model_id: str


# TODO-AT TN: I just copied the model_creation_request,
#         since this class was used but i could not find it
#         please change
class model_function_request(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    model_id: str


# TODO-AT TN: I just copied the model_creation_request,
#         since this class was used but i could not find it
#         please change
class model_update_request(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    model_id: str
    model_specification: dict


class model_creation_request(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    # XXX-TN I puropsefully chose model_specification to be a dict since
    #          using the generic model, would incur the loss of pydantics strengths
    modelType: str
    # XXX-TN For the docker ochestration it will be helpfull to also have an input for
    #        the location of Model initialization (local, local[dockerfile], remote)
    model_specification: dict


@router.get(
    "/implemented",
    response_description="Lists all currently available(implemented) models",
    response_model=storage_controller_list_reponse,
    status_code=status.HTTP_200_OK,
)
def list_all_implemented_models(
    settings: Settings = Depends(get_settings),
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> storage_controller_list_reponse:
    """Endpoint for getting a list of all implemented models"""
    models = []
    for implemented_models in settings.implemented_models:
        for implemented_model in implemented_models.keys():
            models.append(implemented_model)
    return storage_controller_list_reponse(models=models)


@router.get(
    "/{current_model_id}",
    response_description="Lists all function calls of the current model",
    response_model=model_specific_function_call_response,
    status_code=status.HTTP_200_OK,
)
def list_all_function_calls(
    current_model_id: str, sc: storage_controller = Depends(get_storage_controller)
) -> BaseModel:
    """Endpoint for getting a list of all implemented function calls"""
    # validate id
    current_model = sc.get_model(current_model_id)
    if current_model is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not found")

    # get fun calls
    cMFCalls = current_model.get_function_calls()  # current model functioncalls list
    return model_specific_function_call_response(functionCalls=cMFCalls)


@router.delete(
    "/{current_model_id}",
    response_description="Delete the current model",
    response_model=model_deletion_response,
    status_code=status.HTTP_200_OK,
)
def delete_model(
    current_model_id: str, sc: storage_controller = Depends(get_storage_controller)
) -> model_deletion_response:
    """Endpoint for deleting a model"""
    # validate id
    current_model = sc.get_model(current_model_id)
    if current_model is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not implemented")

    # delete it
    sc.del_model(current_model.get_id())
    return model_deletion_response(model_id=current_model_id)


# TODO-AT I could not get this to work/don't understand what needs to be done
#         and i think we should not be calling other endpoint functions
# XXX-AT Some do it like that, but with "FastAPI" and some use just "get" for it.
#        Other question would be, if we actually need this, if we have delete and put.
#        Is there a reason, why we use "API-Router" and not "FastAPI"?
# @router.patch(
#     "/{current_model_id}",
#     response_description="Update the current model",
#     response_model=model_creation_response,
#     status_code=status.HTTP_201_CREATED,
# )
# def updateModel(
#     model_creation_request: model_creation_request, response: Response, current_model_id: str
# ) -> BaseModel:
#     """Endpoint for updating a model"""
#     # validate id
#     current_model = storage.getModel(current_model_id)
#     if current_model is None:
#         # error not found
#         raise HTTPException(status_code=404, detail="Model not implemented")
#
#     # create new, delete old
#     newID = create_model(model_creation_request, response)
#     storage.delModel(current_model.getId())
#     return model_creation_response(modelID=newID)


@router.get(
    "/",
    response_description="Lists all currently created models",
    response_model=storage_controller_list_reponse,
    status_code=status.HTTP_200_OK,
)
def list_all_created_models(
    settings: Settings = Depends(get_settings),
    sc: storage_controller = Depends(get_storage_controller),
) -> storage_controller_list_reponse:
    """Endpoint for getting a list of all created models"""
    all_models = list([str(i) for i in sc.get_all_models()])
    return storage_controller_list_reponse(models=all_models)


@router.post(
    "/",
    response_description="Creates a model",
    response_model=model_creation_response,
    status_code=status.HTTP_201_CREATED,
)
def create_model(
    model_creation_request: model_creation_request,
    response: Response,
    settings: Settings = Depends(get_settings),
    sc: storage_controller = Depends(get_storage_controller),
) -> model_creation_response:
    """Endpoint for creating a model

    Arguments:
        model_creation_request (model_creation_request): A model_creation_request used for the
        creation of the actual model

    Returns:
        dict: Either an error or the created model id
    """
    model = None
    for implemented_models in settings.implemented_models:
        if model_creation_request.modelType in implemented_models:
            model_specs = implemented_models[model_creation_request.modelType]
            model_module = import_module(model_specs[0])  # TODO Use proper model
            model_class = model_specs[1]
            model = getattr(model_module, model_class)(
                type=model_creation_request.modelType,
                **(model_creation_request.model_specification),
            )
    if model is None:
        raise HTTPException(status_code=404, detail="Model not implemented")
    sc.add_model(model)
    response.headers["location"] = f"/api/v{__version__.split('.')[0]}/models/{model.id}"

    return model_creation_response(model_id=model.id)


@router.post(
    "/{current_model_id}",
    response_description="Runs a function",
    response_model=generic_output_model,
    status_code=status.HTTP_200_OK,
)
def getInformation(
    current_model_id: str,
    generic_input: generic_input_model,
    sc: storage_controller = Depends(get_storage_controller),
) -> BaseModel:
    """Gets info out of post data"""
    return run_function(current_model_id, generic_input.function_call, generic_input.input_data, sc)


def run_function(
    current_model_id: str, req_function: str, data_input: Dict[Any, Any], sc: storage_controller
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
        my_fun = getattr(current_model, req_function)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Function not implemented")

    # Run function and parse output dict into actual response model
    output = my_fun(**data_input)
    # XXX-TN we have to ensure that we return a dict on a function call
    #        i dont know if the following is the best way to achive this
    if not type(output) is dict:
        # raise HTTPException(status_code=500, detail="Model did not return a valid response")
        output = {req_function: str(output)}  # TODO-TN this is relly hacky
    out_model_resp = generic_output_model(outputData=output)

    return out_model_resp
