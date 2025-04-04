import re
from .command import Command
from ..fs import Directory
class Ls(Command):
    """
    List the contents of the current directory or the directory at the specified path.
    """

    def __init__(self):
        super().__init__("ls")

    def __call__(self, shell, *args):
        target = shell.current
        show_hidden_flag = False

        if args and args[0] == '-a':
            args = list(args)
            show_hidden_flag = True
            args.pop(0)
        if args:
            paths_regex = r'(^/|^\.{1,2}/|^[^/])([^/\0]+/)*([^/\0]+)?'
            if re.match(paths_regex, args[0]):
                target = shell.current.find(args[0])
        ans = list()
        for item in target:
            if isinstance(item, Directory):
                if item.name.startswith('.'):
                    if show_hidden_flag:
                        ans.append(f'{item.name}/')
                else:
                    ans.append(f'{item.name}/')
            else:
                if item.name.startswith('.'):
                    if show_hidden_flag:
                        ans.append(item.name)
                else:
                    ans.append(item.name)
        return '\n'.join(ans)


    def help(self):
        """
        Display help information for the ls command.
        """
        return "ls [path]\n\nList the contents of the current directory or the directory at the specified path."