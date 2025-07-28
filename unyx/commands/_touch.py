import re
from .._fs import File
from ..errors import Error
from .command import Command
class Touch(Command):
    def __init__(self):
        super().__init__("touch")

    def __call__(self, shell, *args):
        dest_path, name = args[0].strip().rsplit('/', 1)
        dest = shell.current.find(dest_path)
        if isinstance(dest, Error):
            return dest
        for item in dest:
            if item.name == name:
                ans = Error(-5)
                ans.add_description('File already exists')
                return ans
        valid_regex = r'^[^/\\:*?"<>|]+$'
        if re.match(valid_regex, name):
            File(dest, name)
        else:
            ans = Error(-2)
            ans.add_description('Invalid file name')
            return ans