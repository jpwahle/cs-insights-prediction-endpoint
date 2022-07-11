"""This module will forward requests to child nodes"""
import re
from json import JSONDecodeError
from typing import Awaitable, Callable, Optional, TypeVar

import requests
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from nlp_land_prediction_endpoint.utils import settings as Settings
from nlp_land_prediction_endpoint.utils.remote_storage_controller import (
    remote_storage_controller,
)

T = TypeVar("T", bound="ForwardMiddleware")
settings = Settings.get_settings()


class ForwardMiddleware(BaseHTTPMiddleware):
    """Forward middleware which forwards request send to the MAIN Node

    Args:
        BaseHTTPMiddleware (Any): Base class of starlette to create HTTPMiddlware
    """

    async def dispatch(
        self: T, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Forwards requests to the NODEs

        Args:
            request (Request): The request object, as passed down by FastAPI
            call_next (Callable[[Request], Awaitable[Response]]): The function to call next
        Returns:
            Response: A response either from forwarded FROM a NODE or self proccessed response
        """
        if settings.NODE_TYPE == "MAIN":
            try:
                body = await request.json()
            except JSONDecodeError:
                body = {}
            # Check if modelid can be resolved to host
            if "modelType" in body and request.method == "POST":
                host = remote_storage_controller.find_model_in_remote_hosts(body["modelType"])
            else:
                host = get_host(request.url.path)
            # We don't have a model nor a creation request
            if host is None:
                response = await call_next(request)
                return response
            # XXX-TN Maybe it is better/safer to do a if for each possible method?
            r = getattr(requests, request.method.lower())(
                f"http://{host}{request.url.path}", json=body
            )
            response = Response(
                content=r.content, status_code=r.status_code, media_type="application/json"
            )
        else:
            response = await call_next(request)
        return response


def get_host(path: str) -> Optional[str]:
    """Returns the host depending on an url path

    Args:
        path (str): The input path of the request

    Returns:
        Optional[str]: Either {host.ip}:{host.port} if host was found; None otherwise
    """
    url_regex = r"/api/v[0-9]+/models/([0-9]+)/*"
    m = re.match(url_regex, path)
    if m is not None:
        model = m.group(1)
        host = remote_storage_controller.find_active_model_in_remote_hosts(model)
    else:
        host = None
    return host
