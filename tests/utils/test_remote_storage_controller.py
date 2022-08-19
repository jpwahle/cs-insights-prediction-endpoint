"""Test the remote storage controller."""
import pytest

from cs_insights_prediction_endpoint.utils.remote_storage_controller import (
    RemoteStorageController,
)
from cs_insights_prediction_endpoint.utils.settings import get_settings


@pytest.fixture
def dummy_remote_storage_controller() -> RemoteStorageController:
    """Provides a dummy storage controller

    Returns:
        StorageController: empty
    """
    return RemoteStorageController(get_settings())


def test_host_not_found(dummy_remote_storage_controller: RemoteStorageController) -> None:
    output = dummy_remote_storage_controller.get_remote_host("Non-Existent")
    output is None


def test_host_no_created_model_found(
    dummy_remote_storage_controller: RemoteStorageController,
) -> None:
    output = dummy_remote_storage_controller.find_created_model_in_remote_hosts("")
    assert output is None
