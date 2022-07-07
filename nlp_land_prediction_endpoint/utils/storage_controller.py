"""This module implements a storage controller for the endpoint management"""

from typing import Optional, Set, TypeVar

from nlp_land_prediction_endpoint.models.generic_model import GenericModel
from nlp_land_prediction_endpoint.models.model_hosts import RemoteHost

T = TypeVar("T", bound="StorageController")


# XXX-TN This will be only a temporary implementation
#        we should create an Issue for an actual implementation
class StorageController:
    """Storage Controller class to enable access to currently created Models"""

    models: Set[GenericModel] = set([])

    def __init__(self: T) -> None:
        """Constructor for the storage controller"""
        self.models = set([])

    def getModel(self: T, id: str) -> Optional[GenericModel]:
        """Returns the model with id"""
        for model in self.models:
            if model.id == id:
                return model
        return None

    def getAllModels(self: T) -> Set[GenericModel]:
        """Returns all models"""
        return self.models

    def addModel(self: T, model: GenericModel) -> str:
        """Adds model to models"""
        self.models.add(model)
        return model.id

    def delModel(self: T, id: str) -> None:
        """Delete model from storage"""
        model = self.getModel(id)
        if model is None:
            raise KeyError("Model not found")
        else:
            self.models.remove(model)


storage: StorageController = StorageController()

RS = TypeVar("RS", bound="RemoteStorageController")


class RemoteStorageController:
    """StorageController for stroing remote hosts"""

    remote_host_list: Set[RemoteHost] = set(
        [
            RemoteHost(
                **{  # TODO Remove after testing
                    "ip": "127.0.0.1",
                    "port": "8001",
                    "models": ["lda"],
                    "active_models": [],
                }
            )
        ]
    )

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
                return host.ip
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
                return host.ip
        return None

    def remove_remote_host(self: RS, ip: str) -> bool:
        """Remove a host from the remote host list

        Args:
            ip (str): ip of host to remove
        Returns:
            bool: True if host was found and removed; False otherwise
        """
        for i, host in enumerate(self.remote_host_list):
            if host.ip == ip:
                self.remote_host_list.remove(host)
                return True
        return False
