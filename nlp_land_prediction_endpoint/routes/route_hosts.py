"""This module implements the hosts managment"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from nlp_land_prediction_endpoint.models.model_hosts import RemoteHost
from nlp_land_prediction_endpoint.utils.remote_storage_controller import (
    RemoteStorageController,
    get_remote_storage_controller,
)

router: APIRouter = APIRouter()


class RemoteHostDeleteRequest(BaseModel):
    """Request/Response model for host deletion requests"""

    ip: str


class RemoteHostListResponse(BaseModel):
    """Response model for host listing all hosts"""

    remote_host_list: List[RemoteHost]


@router.get(
    "/",
    response_description="Get all currently available hosts",
    response_model=RemoteHostListResponse,
    status_code=status.HTTP_200_OK,
)
def list_all_remote_hosts(
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> RemoteHostListResponse:
    """List all remote hosts

    Returns:
        RemoteHostListResponse: List of all currently registered remote hosts.
    """
    return RemoteHostListResponse(remote_host_list=rsc.get_all_remote_hosts())


@router.post(
    "/",
    response_description="Get all currently available hosts",
    response_model=RemoteHost,
    status_code=status.HTTP_200_OK,
)
def add_remote_host(
    remote_host: RemoteHost, rsc: RemoteStorageController = Depends(get_remote_storage_controller)
) -> RemoteHost:
    """Add a remote host to the remote host list

    Args:
        remote_host (RemoteHost): The remote host to add

    Returns:
        RemoteHost: The added remote host
    """
    rsc.add_remote_host(remote_host)
    return remote_host


@router.delete(
    "/",
    response_description="Get all currently available hosts",
    response_model=RemoteHostDeleteRequest,
    status_code=status.HTTP_200_OK,
)
def delete_remote_host(
    to_delete: RemoteHostDeleteRequest,
    rsc: RemoteStorageController = Depends(get_remote_storage_controller),
) -> RemoteHostDeleteRequest:
    """Delete a remote host from the remote host list

    Args:
        remote_host (RemoteHost): The remote host to delete

    Returns:
        RemoteHost: The deleted remote host
    """
    if not rsc.remove_remote_host(to_delete.ip):
        raise HTTPException(status_code=404, detail="Host not found")
    return to_delete
