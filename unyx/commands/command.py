from __future__ import annotations

from abc import abstractmethod, ABCMeta
from ..errors import Error


class Shell:
    ...


class Command(metaclass=ABCMeta):
    """
    Base class for all commands.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __call__(self, shell:Shell, *args) -> Error | str:
        """
        Execute the command.
        """
        raise NotImplementedError("Subclasses must implement this method.")
