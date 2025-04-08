from .command import Command
from ..errors import Error

class Mv(Command):
    def __init__(self):
        super().__init__("mv")
    def __call__(self, shell,  *args):
        target = shell.current.find(args[0])
        dest = shell.current.find(args[1])
        if isinstance(target, Error):
            target.add_description('Invalid target')
            return target
        if isinstance(dest, Error):
            dest.add_description('Destination not found')
            return dest
        for item in dest.child:
            if item.name == target.name:
                ans = Error(-2)
                ans.add_description('File already exists')
                return ans
        target.move(dest)
    
    def help(self):
        return "mv [src] [dest]"