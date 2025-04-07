from .command import Command
from ..fs import File
from ..errors import Error
class Grep(Command):
    def __init__(self):
        super().__init__("grep")

    def __call__(self, shell, *args):
        filepath = args[-1]
        file: File | Error = shell.current.find(filepath)
        if isinstance(file, Error):
            return file
        args = args[:-1]
        return file.grep(*args)
    
    def help(self):
        """
        Display help information for the grep command.
        """
        return "grep [pattern] [file]\n\nSearch for a pattern in a file."