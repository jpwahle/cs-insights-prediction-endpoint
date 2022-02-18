"""This module implements the endpoint logic for models."""
from typing import List

from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel

from nlp_land_prediction_endpoint import __version__
from nlp_land_prediction_endpoint.models.lda_model import LDAModel
from nlp_land_prediction_endpoint.utils.storage_controller import storage
from nlp_land_prediction_endpoint.models.generic_model import GenericOutputModel

router: APIRouter = APIRouter()


class StorageControllerListReponse(BaseModel):
    """Response model for both
        - GET /
        - GET /implemented
    which returns a list of models
    """

    models: List[str]
    functionCalls: List[str]
    # error: str


class ErrorModel(BaseModel):
    """Response Model for an err0r"""

    error: str


class ModelCreationResponse(BaseModel):
    """Response Model for the successfull creation of a model"""

    modelID: str


class ModelOutputResponse(BaseModel):
    output_model: GenericOutputModel


class ModelCreationRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    # XXX-TN I puropsefully chose modelSpecification to be a dict since
    #          using the generic model, would incur the loss of pydantics strengths
    modelType: str
    # XXX-TN For the docker ochestration it will be helpfull to also have an input for
    #        the location of Model initialization (local, local[dockerfile], remote)
    modelSpecification: dict


@router.get(
    "/{current_modelID}",
    response_description="Lists all function calls of the current model",
    response_model=BaseModel,
    status_code=status.HTTP_200_OK,
)
def list_all_function_calls(current_modelID: str) -> BaseModel:
    """Endpoint for getting a list of all implemented function calls"""
    # validate id
    currentModel = storage.getModel(current_modelID)
    if currentModel is None:
        # error not found
        return ErrorModel(error="NotFound")

    # get fun calls
    cMFCalls = currentModel.getFunctionCalls()  # current model functioncalls list
    return StorageControllerListReponse(functionCalls=[cMFCalls])


@router.delete(
    "/{current_modelID}",
    response_description="Delete the current model",
    response_model=StorageControllerListReponse,  # still applicable?
    status_code=status.HTTP_200_OK,
)
def deleteModel(current_modelID: str) -> BaseModel:
    """Endpoint for deleting a model"""
    # validate id
    currentModel = storage.getModel(current_modelID)
    if currentModel is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not implemented")

    # delete it
    storage.delModel(currentModel.getId())
    return BaseModel(data="done")


@router.patch(
    "/{current_modelID}",
    response_description="Update the current model",
    response_model=ModelCreationResponse,
    status_code=status.HTTP_201_CREATED,
)
def updateModel(modelCreationRequest: ModelCreationRequest, response: Response, current_modelID: str) -> BaseModel:
    """Endpoint for updating a model"""
    # validate id
    currentModel = storage.getModel(current_modelID)
    if currentModel is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not implemented")

    # create new, delete old
    newID = create_model(modelCreationRequest, response)
    storage.delModel(currentModel.getId())
    return ModelCreationResponse(modelID=newID)


@router.get(
    "/implemented",
    response_description="Lists all currently available(implemented) models",
    response_model=StorageControllerListReponse,
    status_code=status.HTTP_200_OK,
)
def list_all_implemented_models() -> StorageControllerListReponse:
    """Endpoint for getting a list of all implemented models"""
    return StorageControllerListReponse(models=["lda"])


@router.get(
    "/",
    response_description="Lists all currently created models",
    response_model=StorageControllerListReponse,
    status_code=status.HTTP_200_OK,
)
def list_all_created_models() -> StorageControllerListReponse:
    """Endpoint for getting a list of all created models"""
    all_models = list([str(i) for i in storage.getAllModels()])
    return StorageControllerListReponse(models=all_models)


@router.post(
    "/",
    response_description="Creates a model",
    response_model=ModelCreationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_model(
    modelCreationRequest: ModelCreationRequest, response: Response
) -> ModelCreationResponse:
    """Endpoint for creating a model

    Arguments:
        modelCreationRequest (ModelCreationRequest): A ModelCreationRequest used for the creation
                                                 of the actual model

    Returns:
        dict: Either an error or the created model id
    """
    model = None
    if modelCreationRequest.modelType == "lda":
        model = LDAModel(**modelCreationRequest.modelSpecification)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not implemented")
    storage.addModel(model)
    response.headers["location"] = f"/api/v{__version__.split('.')[0]}/models/{model.id}"

    return ModelCreationResponse(modelID=model.id)


@router.post(
    "/{current_modelID}/{req_function}/{data_input}",
    response_description="Runs a function",
    response_model=GenericOutputModel,
    status_code=status.HTTP_200_OK,
)
def run_function(current_modelID: str, req_function: str, data_input: str) -> BaseModel:
    # validate id
    currentModel = storage.getModel(current_modelID)
    if currentModel is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not implemented")

    # validate function call
    function = ""
    for i in currentModel.getFunctionCalls():
        if (i == req_function):
            function = currentModel.getFunctionCalls()[i]
            break

    if (function == ""):
        raise HTTPException(status_code=404, detail="Function of model not implemented")

    # select right function
    # Something like:
    #   currentmodel.{function}()

    # Find function, it will be stored in myFun
    try:
        myFun = getattr(currentModel, function)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Function not implemented")

    # Call the function with input
    output = myFun(data_input)
    outModelResp = ModelOutputResponse(output_model=output)

    # return
    return outModelResp