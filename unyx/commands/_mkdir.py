import re
from .command import Command
from ..errors import Error
from .._fs import Directory

class Mkdir(Command):
    def __init__(self):
        super().__init__("mkdir")

    def __call__(self, shell, *args):
        if '/' in args[0]:
            dest_path, name = args[0].strip().rsplit('/', 1)
        else:
            dest_path, name = '.', args[0].strip()
        dest = shell.current.find(dest_path)
        if isinstance(dest, Error):
            return dest
        for item in dest:
            if item.name == name:
                ans = Error(-5)
                ans.add_description('File already exists')
                return ans
        valid_regex = r'^[^/\\:*?"<>|.\^]+$'
        if re.match(valid_regex, name):
            Directory(dest, name)
        else:
            ans = Error(-2)
            ans.add_description('Invalid file name')
            return ans