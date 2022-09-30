from typing import Any

import pytest
import requests
from requests.models import Response

from cs_insights_prediction_endpoint.utils import settings
from cs_insights_prediction_endpoint.utils.version_getter import get_backend_version


@pytest.fixture
def mock_version_request(monkeypatch: Any) -> None:
    """Simulates request.get by overwriting the function

    Arguments:
        monkeypatch: a monkeypatch object
    """

    def mock_get(*args, **kwargs):
        # type: (*str, **int) -> Response
        response = Response()
        response.status_code = 200
        response._content = b'{"__v": 0}'
        return response

    monkeypatch.setattr(requests, "get", mock_get)


def test_missing_backend_version(monkeypatch: Any, mock_version_request: Any) -> None:
    settings.get_settings().auth_backend_version = ""
    get_backend_version()
