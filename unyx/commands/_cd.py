from .command import Command
from ..fs import _ContainerFSObject
from ..errors import Error
class Cd(Command):
    def __init__(self):
        super().__init__("cd")

    def __call__(self, shell, *args):
        """
        Change the current directory to the specified path.

        Args:
            `shell` : The shell instance.
            `*args`: The arguments passed to the command.

        """
        if args:
            target = shell.current.find(args[0])
        else:
            target = shell.root # TODO: Change to home directory
        if isinstance(target, Error):
            return target
        elif not isinstance(target, _ContainerFSObject):
            ans = Error(-5)
            ans.add_description('Not a directory')
            return ans
        else:
            shell.current = target