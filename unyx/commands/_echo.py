from .command import Command
from ..errors import Error


class Echo(Command):
    def __init__(self):
        super().__init__("echo")
        
    def __call__(self, shell, *args):
        ans = list()
        for arg in args:
            if '$' not in arg:
                ans.append(arg)
            else:
                if arg[arg.index('$') - 1] == '\\':
                    ans.append(arg.replace('\\$', '$'))
                else:
                    if arg[arg.index('$') + 1] == '{':
                        var = arg[arg.index('{') + 1 : arg.index('}')]
                        arg = arg.replace(
                            f'${{{var}}}', shell.current.root.get_var(var)
                        )
                    else:
                        var = arg[arg.index('$') + 1 :]
                        arg = arg.replace(
                            f'${var}', shell.current.root.get_var(var)
                        )
                    ans.append(arg)
        return ' '.join(ans)