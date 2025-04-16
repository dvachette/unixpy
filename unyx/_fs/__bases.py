from abc import ABC, abstractmethod
from typing import Iterator
class _FSObject(ABC):
    @abstractmethod
    def path(self):
        """
        Returns the path of the object.
        """
        pass


    pass

class _ContainerFSObject(_FSObject, ABC):

    @abstractmethod
    def __len__(self) -> int:
        """
        Returns the number of FS Objects in the container.
        """
        pass
    
    @abstractmethod
    def __iter__(self) -> Iterator[_FSObject]:
        """
        Returns an iterator over the FS Objects in the container.
        """
        pass

    @abstractmethod
    def __contains__(self, value:str) -> bool:
        """
        Checks if the container contains an FS Object with the same name as the given FS Object.
        """
        pass
    
    @abstractmethod
    def find(self, path: str) -> _FSObject:
        """
        Finds the FS Object at the given path.
        """

