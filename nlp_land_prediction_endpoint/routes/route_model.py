"""This module implements the endpoint logic for models."""
from typing import List

from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel

from nlp_land_prediction_endpoint import __version__
from nlp_land_prediction_endpoint.models.generic_model import GenericOutputModel
from nlp_land_prediction_endpoint.models.lda_model import LDAModel
from nlp_land_prediction_endpoint.utils.storage_controller import storage

router: APIRouter = APIRouter()


class StorageControllerListReponse(BaseModel):
    """Response model for both
        - GET /
        - GET /implemented
    which returns a list of models
    """

    models: List[str]
    # error: str


class ModelSpecificFunctionCallResponse(BaseModel):
    """Response model for model specific function calls"""

    functionCalls: List[str]


# XXX-TN Do we need this?
# XXX-AT We can just output every error with status-codes, but they are not precise
#class ErrorModel(BaseModel):
#    """Response Model for an error"""
#
#    error: str


class ModelCreationResponse(BaseModel):
    """Response Model for the successfull creation of a model"""

    modelID: str


class ModelDeletionResponse(BaseModel):
    """Response Model for the successfull deletion of a model"""

    modelID: str


class ModelOutputResponse(BaseModel):
    """Response Model for an output of function of a model"""

    # XXX-TN This needs some more explaing
    # output_model: GenericOutputModel
    # For now i changed it to a simple string output
    # XXX-AT if we have as Output something like a list, a model would be more gerneral, but str is fine
    output: str


# TODO-AT TN: I just copied the ModelCreationRequest,
#         since this class was used but i could not find it
#         please change
class ModelDeletionRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    modelID: str


# TODO-AT TN: I just copied the ModelCreationRequest,
#         since this class was used but i could not find it
#         please change
class ModelFunctionRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    modelID: str


# TODO-AT TN: I just copied the ModelCreationRequest,
#         since this class was used but i could not find it
#         please change
class ModelUpdateRequest(BaseModel):
    """Response model for creating a Model
    This contains the modelType (e.g., lda) and the model specification
    which should be parsable to the modelTypes pydentic schema.
    """

    modelID: str
    modelSpecification: dict


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
    "/implemented",
    response_description="Lists all currently available(implemented) models",
    response_model=StorageControllerListReponse,
    status_code=status.HTTP_200_OK,
)
def list_all_implemented_models() -> StorageControllerListReponse:
    """Endpoint for getting a list of all implemented models"""
    return StorageControllerListReponse(models=["lda"])


@router.get(
    "/{current_modelID}",
    response_description="Lists all function calls of the current model",
    response_model=ModelSpecificFunctionCallResponse,
    status_code=status.HTTP_200_OK,
)
def list_all_function_calls(current_modelID: str) -> BaseModel:
    """Endpoint for getting a list of all implemented function calls"""
    # validate id
    currentModel = storage.getModel(current_modelID)
    if currentModel is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not found")

    # get fun calls
    cMFCalls = currentModel.getFunctionCalls()  # current model functioncalls list
    return ModelSpecificFunctionCallResponse(functionCalls=cMFCalls)


@router.delete(
    "/{current_modelID}",
    response_description="Delete the current model",
    response_model=ModelDeletionResponse,
    status_code=status.HTTP_200_OK,
)
def deleteModel(current_modelID: str) -> ModelDeletionResponse:
    """Endpoint for deleting a model"""
    # validate id
    currentModel = storage.getModel(current_modelID)
    if currentModel is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not implemented")

    # delete it
    storage.delModel(currentModel.getId())
    return ModelDeletionResponse(modelID=current_modelID)


# TODO-AT I could not get this to work/don't understand what needs to be done
#         and i think we should not be calling other endpoint functions
# XXX-AT Some do it like that, but with "FastAPI" and some use just "get" for it.
#        Other question would be, if we actually need this, if we have delete and put.
#        Is there a reason, why we use "API-Router" and not "FastAPI"?
# @router.patch(
#     "/{current_modelID}",
#     response_description="Update the current model",
#     response_model=ModelCreationResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def updateModel(
#     modelCreationRequest: ModelCreationRequest, response: Response, current_modelID: str
# ) -> BaseModel:
#     """Endpoint for updating a model"""
#     # validate id
#     currentModel = storage.getModel(current_modelID)
#     if currentModel is None:
#         # error not found
#         raise HTTPException(status_code=404, detail="Model not implemented")
#
#     # create new, delete old
#     newID = create_model(modelCreationRequest, response)
#     storage.delModel(currentModel.getId())
#     return ModelCreationResponse(modelID=newID)


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


# XXX-TN I think we should consider putting req_function and data_input as post parameters
#        rather than using them as query parameters. Especially for data_input this makes
#        much more sense
# XXX-AT Makes sense
@router.post(
    "/{current_modelID}",
    response_description="Runs a function",
    response_model=GenericOutputModel,
    status_code=status.HTTP_200_OK,
)
async def getInformation(current_modelID: str, info : Request) -> BaseModel:
    """gets info out of post data"""
    req_info = await info.json()
    req_function = req_info["function"]
    data_input = req_info["data"] 
    return run_function(current_modelID, req_function, data_input)
    

def run_function(current_modelID: str, req_function: str, data_input: str) -> BaseModel:
    """Runs a given function of a given model"""
    # validate id
    currentModel = storage.getModel(current_modelID)
    if currentModel is None:
        # error not found
        raise HTTPException(status_code=404, detail="Model not implemented")

    # select right function
    # something like:
    #   currentmodel.{function}()

    # Find function, it will be stored in myFun
    try:
        myFun = getattr(currentModel, req_function)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Function not implemented")

    # Call the function with input
    # output = myFun(data_input)
    # XXX-TN The above call will almost never work due to data_input being a string.
    #        I think a good solution would be to define data_input as dict and upack it here
    # XXX-AT Now with info from request working?
    output = myFun()  # Temporary see above
    outModelResp = ModelOutputResponse(output=str(output))

    # return
    return outModelResp
