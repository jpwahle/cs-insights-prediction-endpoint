"""This module implements a remote storage controller for the endpoint management"""

from functools import lru_cache
from typing import List, Optional, TypeVar

import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection

from cs_insights_prediction_endpoint.models.model_hosts import remote_host
from cs_insights_prediction_endpoint.utils.settings import Settings, get_settings

RS = TypeVar("RS", bound="remote_storage_controller")

# Attributes to exclude when saving pydentic models to the database
# exclude_attributes: Any = {}


class remote_storage_controller:
    """StorageController for stroing remote hosts"""

    remote_host_list: List[RemoteHost] = []

    def __init__(self: RS, settings: Settings) -> None:
        """Constructor for the remote storage controller

        Args:
            settings (Settings): Settings object used for information on the databse
        """
        self.remote_host_client: MongoClient = pymongo.MongoClient(
            f"mongodb://{settings.mongo_user.get_secret_value()}"
            + f":{settings.mongo_password.get_secret_value()}@{settings.mongo_host}",
        )
        self.remote_host_db: Collection = self.remote_host_client[settings.remote_host_db_name][
            settings.remote_host_db_name
        ]

    def get_all_models(self: RS) -> List[str]:
        """Returns all implemented models from every host

        Returns:
            List[str]: The list of all currently created models
        """
        all_models = []
        for host in self.remote_host_list:
            for model in host.models:
                all_models.append(model)
        return all_models

    def get_all_created_models(self: RS) -> List[str]:
        """Returns all currently created models from every host

        Returns:
            List[str]: The list of all currently created models
        """
        all_created_models = []
        for host in self.remote_host_list:
            for model in host.created_models:
                all_created_models.append(model)
        return all_created_models

    def get_all_remote_hosts(self: RS) -> List[remote_host]:
        """Returns all remote hosts currently in the remote_host_list

        Returns:
            Set[remote_host]: The set of all currently added remote hosts
        """
        return self.remote_host_list

    def get_remote_host(self: RS, ip: str) -> Optional[remote_host]:
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

    def add_model_to_created_model_list(self: RS, ip: str, model_id: str) -> None:
        """Adds a newly created model to the list of remote models"""
        r_host: Optional[remote_host] = self.get_remote_host(ip)
        if r_host is not None:
            r_host.created_models.append(model_id)
            self.remote_host_db.update_one({"ip": ip}, {"$set": r_host.dict()})

    def remove_model_from_created_model_list(self: RS, ip: str, model_id: str) -> None:
        """Removes a created model from the list of remote models"""
        r_host: Optional[remote_host] = self.get_remote_host(ip)
        if r_host is not None:
            r_host.created_models.remove(model_id)
            self.remote_host_db.update_one({"ip": ip}, {"$set": r_host.dict()})

    def find_created_model_in_remote_hosts(self: RS, to_search: str) -> Optional[str]:
        """Returns the ip of the remote hosts containing the created_model 'to_search'

        Args:
            to_search (str): An created model id
        Returns:
            Optional[str]: The ip of the host if it was found; None otherwise
        """
        for host in self.remote_host_list:
            if to_search in host.created_models:
                return f"{host.ip}:{host.port}"
        return None

    def find_model_in_remote_hosts(self: RS, to_search: str) -> Optional[str]:
        """Returns the ip of the remote hosts containing the model 'to_search'

        Args:
            to_search (str): A model string
        Returns:
            Optional[str]: The ip of the host if it was found; None otherwise
        """
        for host in self.remote_host_list:
            if to_search in host.models:
                return f"{host.ip}:{host.port}"
        return None

    def add_remote_host(self: RS, to_add: remote_host) -> remote_host:
        """Add a remote host to the list

        Args:
            to_add (remote_host): Host to add

        Returns:
            remote_host: The host that was added; or None on failure
        """
        # self.remote_host_db.insert_one(to_add.dict(exclude=exclude_attributes))
        self.remote_host_db.insert_one(to_add.dict())
        self.remote_host_list.append(to_add)
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
                self.remote_host_db.delete_one({"ip": ip})
                self.remote_host_list.remove(host)
                return True
        return False


# remote_storage_controller: remote_storage_controller = remote_storage_controller(get_settings())


@lru_cache()
def get_remote_storage_controller() -> remote_storage_controller:
    """Return the remote_storage_controller instance"""
    return remote_storage_controller(get_settings())
    # return remote_storage_controller
