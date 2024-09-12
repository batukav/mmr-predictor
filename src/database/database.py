from abc import ABC
from abc import abstractmethod


class database(ABC):

    @abstractmethod
    def get_collection():
        pass

    @abstractmethod
    def insert_item():
        pass

    @abstractmethod
    def get_item():
        pass
