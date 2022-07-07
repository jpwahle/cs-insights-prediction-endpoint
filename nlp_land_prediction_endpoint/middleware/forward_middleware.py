"""This module will forward requests to child nodes"""
from typing import Awaitable, Callable, TypeVar

import requests
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from nlp_land_prediction_endpoint.utils.settings import get_settings

T = TypeVar("T", bound="ForwardMiddleware")
settings = get_settings()


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
            # XXX-TN Maybe it is better/safer to do a if for each possible method?
            r = getattr(requests, request.method.lower())(
                f"http://127.0.0.1:8001{request.url.path}"
            )
            response = Response(
                content=r.content, status_code=r.status_code, media_type="application/json"
            )
        else:
            response = await call_next(request)
        return response
