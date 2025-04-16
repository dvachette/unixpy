from .command import Command
from .._fs import _FSObject, _ContainerFSObject
from ..errors import Error


class Cut(Command):

    def __init__(self):
        super().__init__("cut")


    def __call__(self, shell, *args):
        if len(args) < 4:
            ans = Error(-3)
            ans.add_description('Missing arguments')
            return ans
        filepath = args[-1]
        file: _FSObject | Error = shell.current.find(filepath)
        if isinstance(file, Error):
            return file
        if isinstance(file, _ContainerFSObject):
            ans = Error(-5)
            ans.add_description(f"{filepath} is not a file")
            return ans

        sep = None
        fields = None

        i = 0
        l = len(args)
        while i < l:
            if args[i] == '-d':
                sep = args[i + 1]
                i += 2
            elif args[i] == '-f':
                fields = args[i + 1]
                i += 2
            else:
                i += 1
        if sep is None or fields is None:
            ans = Error(-3)
            ans.add_description('Missing either -d or -f option')
            return ans
        
        ans = file.cut(sep, fields)
        return ans