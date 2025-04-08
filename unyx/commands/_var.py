from .command import Command
from ..errors import Error

class Var(Command):
    def __init__(self):
        super().__init__("var")

    def __call__(self, shell, *args):
        if args:
            if args[0] == 'list':
                return '\n'.join(shell.current.root.vars.keys())
            elif args[0] == 'dict':
                return '\n'.join(
                    [f'{key} = {value}' for key, value in shell.current.root.vars.items()]
                )
            elif len(args) >= 2:
                match args[0]:
                    case 'set':
                        shell.current.root.vars[args[1]] = ' '.join(args[2:])
                    case 'get':
                        return shell.current.root.get_var(args[1])
                    case 'del':
                        shell.current.root.remove_var(args[1])