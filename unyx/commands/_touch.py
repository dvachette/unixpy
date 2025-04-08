import re
from..fs import File
from ..errors import Error
from .command import Command

class Touch(Command):
    def __init__(self):
        super().__init__("touch")

    def __call__(self, shell, *args):
        for item in shell.current:
            if item.name == args[0]:
                ans = Error(-5)
                ans.add_description('File already exists')
                return ans
        valid_regex = r'^[^/\\:*?"<>|]+$'
        if re.match(valid_regex, args[0]):
            File(shell.current, args[0])
        else:
            ans = Error(-2)
            ans.add_description('Invalid file name')
            return ans