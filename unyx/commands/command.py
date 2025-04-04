from abc import abstractmethod, ABCMeta

class Command(metaclass=ABCMeta):
    """
    Base class for all commands.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __call__(self, shell, *args):
        """
        Execute the command.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def help(self):
        """
        Display help information for the command.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    