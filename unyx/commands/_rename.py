import re

from ..errors import Error
from .command import Command
from .._fs import Root


class Rename(Command):
    def __init__(self):
        super().__init__("rn")
    
    def __call__(self, shell, *args):
        target = shell.current.find(args[0])
        name = args[1]
        name_regex = r'^[^/\\:*?"<>|]+$'
        if not re.match(name_regex, name):
            ans = Error(-2)
            ans.add_description('Invalid name')
            return ans
        if isinstance(target, Error):
            return target
        if isinstance(target, Root):
            ans = Error(-5)
            ans.add_description("Cannot rename root")
            return ans
        target.rename(args[1])