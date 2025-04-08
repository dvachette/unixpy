import re
from .command import Command
from ..errors import Error
from ..fs import Directory

class Mkdir(Command):
    def __init__(self):
        super().__init__("mkdir")

    def __call__(self, shell, *args):
        for item in shell.current:
            if item.name == args[0]:
                ans = Error(-2)
                ans.add_description('Directory already exists')
                return ans
        valid_regex = r'^[^/\\:*?"<>|\s]+$'
        if re.match(valid_regex, args[0]):
            if not all([char == '.' for char in args[0]]):
                Directory(shell.current, args[0])
            else:
                ans = Error(-2)
                ans.add_description('Invalid directory name')
                return ans
        else:
            ans = Error(-2)
            ans.add_description('Invalid directory name')
            return ans