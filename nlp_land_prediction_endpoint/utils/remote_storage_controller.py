"""This module implements a remote storage controller for the endpoint management"""

from typing import Any, List, Optional, Set, TypeVar

from pymongo import MongoClient
from pymongo.collection import Collection

from nlp_land_prediction_endpoint.models.model_hosts import RemoteHost
from nlp_land_prediction_endpoint.utils.settings import Settings, get_settings

RS = TypeVar("RS", bound="RemoteStorageController")

# Attributes to exclude when saving pydentic models to the database
exclude_attributes: Any = {}


class RemoteStorageController:
    """StorageController for stroing remote hosts"""

    remote_host_list: Set[RemoteHost] = set(
        [
            RemoteHost(
                **{  # TODO Remove after testing
                    "ip": "127.0.0.1",
                    "port": "8001",
                    "models": ["lda"],
                    "active_models": ["1234"],
                }
            )
        ]
    )

    def __init__(self: RS, settings: Settings) -> None:
        """Constructor for the remote storage controller

        Args:
            settings (Settings): Settings object used for information on the databse
        """
        self.remote_host_client: MongoClient = MongoClient(settings.REMOTE_HOST_DB_URL)
        self.remote_host_db: Collection = self.remote_host_client[settings.REMOTE_HOST_DB_NAME][
            settings.REMOTE_HOST_DB_NAME
        ]
        print(f"Successful connection to {settings.REMOTE_HOST_DB_URL}")

    def get_all_models(self: RS) -> List[str]:
        """Returns all implemented models from every host

        Returns:
            List[str]: The list of all currently active models
        """
        all_models = []
        for host in self.remote_host_list:
            for model in host.models:
                all_models.append(model)
        return all_models

    def get_all_active_models(self: RS) -> List[str]:
        """Returns all currently active models from every host

        Returns:
            List[str]: The list of all currently active models
        """
        all_active_models = []
        for host in self.remote_host_list:
            for model in host.active_models:
                all_active_models.append(model)
        return all_active_models

    def get_all_remote_hosts(self: RS) -> Set[RemoteHost]:
        """Returns all remote hosts currently in the remote_host_list

        Returns:
            Set[RemoteHost]: The set of all currently added remote hosts
        """
        return self.remote_host_list

    def get_remote_host(self: RS, ip: str) -> Optional[RemoteHost]:
        """Returns the remote hosts specified by ip
        Args:
            ip (str): The ip address of the host to return
        Returns:
            Optional[Remove]: The remote host if it was found; None otherwise
        """
        for i, host in enumerate(self.remote_host_list):
            if host.ip == ip:
                return host
        return None

    def find_active_model_in_remote_hosts(self: RS, to_search: str) -> Optional[str]:
        """Returns the ip of the remote hosts containing the active_model 'to_search'

        Args:
            to_search (str): An active model id
        Returns:
            Optional[str]: The ip of the host if it was found; None otherwise
        """
        for host in self.remote_host_list:
            if to_search in host.active_models:
                return f"{host.ip}:{host.port}"
        return None

    def find_model_in_remote_hosts(self: RS, to_search: str) -> Optional[str]:
        """Returns the ip of the remote hosts containing the model 'to_search'

        Args:
            to_search (str): An active model id
        Returns:
            Optional[str]: The ip of the host if it was found; None otherwise
        """
        for host in self.remote_host_list:
            if to_search in host.models:
                return f"{host.ip}:{host.port}"
        return None

    def add_remote_host(self: RS, to_add: RemoteHost) -> RemoteHost:
        """Add a remote host to the list

        Args:
            to_add (RemoteHost): Host to add

        Returns:
            RemoteHost: The host that was added; or None on failure
        """
        self.remote_host_db.insert_one(to_add.dict(exclude=exclude_attributes))
        self.remote_host_list.add(to_add)  # TODO Check if actually added
        return to_add

    def remove_remote_host(self: RS, ip: str) -> bool:
        """Remove a host from the remote host list

        Args:
            ip (str): ip of host to remove
        Returns:
            bool: True if host was found and removed; False otherwise
        """
        for i, host in enumerate(self.remote_host_list):
            if host.ip == ip:
                self.remote_host_db.delete_one({"ip": ip})  # TODO check if actually deleted
                self.remote_host_list.remove(host)
                return True
        return False


remote_storage_controller: RemoteStorageController = RemoteStorageController(get_settings())


def get_remote_storage_controller() -> RemoteStorageController:
    """Return the remote_storage_controller instance"""
    return remote_storage_controller
