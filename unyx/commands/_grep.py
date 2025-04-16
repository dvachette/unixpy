from .command import Command
from .._fs import File
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