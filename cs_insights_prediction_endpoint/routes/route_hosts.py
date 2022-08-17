"""This module implements the hosts managment"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from cs_insights_prediction_endpoint.models.model_hosts import remote_host
from cs_insights_prediction_endpoint.utils.remote_storage_controller import (
    get_remote_storage_controller,
    remote_storage_controller,
)

router: APIRouter = APIRouter()


class remote_host_delete_request(BaseModel):
    """Request/Response model for host deletion requests"""

    ip: str


class remote_host_list_response(BaseModel):
    """Response model for host listing all hosts"""

    remote_host_list: List[remote_host]


@router.get(
    "/",
    response_description="Get all currently available hosts",
    response_model=remote_host_list_response,
    status_code=status.HTTP_200_OK,
)
def list_all_remote_hosts(
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> remote_host_list_response:
    """List all remote hosts

    Returns:
        remote_host_list_response: List of all currently registered remote hosts.
    """
    return remote_host_list_response(remote_host_list=rsc.get_all_remote_hosts())


@router.post(
    "/",
    response_description="Get all currently available hosts",
    response_model=remote_host,
    status_code=status.HTTP_200_OK,
)
def add_remote_host(
    remote_host: remote_host,
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> remote_host:
    """Add a remote host to the remote host list

    Args:
        remote_host (remote_host): The remote host to add

    Returns:
        remote_host: The added remote host
    """
    rsc.add_remote_host(remote_host)
    return remote_host


@router.delete(
    "/",
    response_description="Get all currently available hosts",
    response_model=remote_host_delete_request,
    status_code=status.HTTP_200_OK,
)
def delete_remote_host(
    to_delete: remote_host_delete_request,
    rsc: remote_storage_controller = Depends(get_remote_storage_controller),
) -> remote_host_delete_request:
    """Delete a remote host from the remote host list

    Args:
        remote_host (remote_host): The remote host to delete

    Returns:
        remote_host: The deleted remote host
    """
    if not rsc.remove_remote_host(to_delete.ip):
        raise HTTPException(status_code=404, detail="Host not found")
    return to_delete
