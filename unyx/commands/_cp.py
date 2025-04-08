from .command import Command
from ..errors import Error
import re
class Cp(Command):
    def __init__(self):
        super().__init__("cp")

    def __call__(self, shell, *args):
        target = shell.current.find(args[0])
        if isinstance(target, Error):
            return target
        if '/' in args[1]:
            dest, name = args[1].rsplit('/', 1)
        else:
            dest, name = '.', args[1]
        name_regex = r'^[^/\\:*?"<>|]+$'
        if not re.match(name_regex, name):
            ans = Error(-2)
            ans.add_description('Invalid name')
            return ans
        dest = shell.current.find(dest)
        copy = target.copy()
        copy.rename(name)
        copy.move(dest)