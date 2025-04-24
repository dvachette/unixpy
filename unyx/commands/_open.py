from .command import Command
from ..errors import Error
from .._fs import File, _ContainerFSObject


class Open(Command):
    def __init__(self):
        super().__init__("open")

    def __call__(self, shell, *args):
        r"""
        `open -m <mode> -b <begin_line> [[-e <end_line>] [-c <content>]] [-l <line>] <path>`

        the content can be multiline, just use \n to separate the lines

        modes:

        r: read

        `open -m r -b <begin_line> -e <end_line> <path>`

        w: write

        `open -m w -c <content> <path>`

        a: append

        `open -m a -c <content> <path>`

        e: edit

        `open -m e -l <line> -c <content> <path>`

        i: insert

        `open -m i -l <line> -c <content> <path>`

        d: delete

        `open -m d -l <line> <path>`
        """

        if len(args) < 1:
            return "Invalid syntax, use 'help open' for more information"
        current = shell.current
        target: File = current.find(args[-1])

        if isinstance(target, Error):
            return target

        if isinstance(target, _ContainerFSObject):
            ans = Error(-5)
            ans.add_description(f"{args[-1]} is not a file")
        mode = None
        begin = 0
        end = None
        line = None
        content = None
        ind = 0
        ans = None
        while ind < len(args) - 1:
            elem = args[ind]
            match elem:
                case '-m':
                    try:
                        mode = args[ind + 1]
                    except IndexError:
                        return 'Missing param after -m'
                    else:
                        if mode not in ['r', 'w', 'a', 'e', 'i', 'd']:
                            return "Invalid mode, use 'help open' for more information"
                    ind += 1
                case '-b':
                    try:
                        begin = int(args[ind + 1])
                    except IndexError:
                        return 'Missing param after -b'
                    except ValueError:
                        return 'Invalid value for -b, must be an integer'
                    ind += 1
                case '-e':
                    try:
                        end = int(args[ind + 1])
                    except IndexError:
                        return 'Missing param after -e'
                    except ValueError:
                        return 'Invalid value for -e, must be an integer'
                    ind += 1
                case '-l':
                    try:
                        line = int(args[ind + 1] - 1)
                    except IndexError:
                        return 'Missing param after -l'
                    except ValueError:
                        return 'Invalid value for -l, must be an integer'
                    ind += 1
                case '-c':
                    try:
                        content_arg = args[ind + 1]
                    except IndexError:
                        return 'Missing param after -c'
                    else:
                        content_arg = content_arg.split(' ')
                        content = list()
                        for elem in content_arg:
                            if '$' not in elem:
                                content.append(elem)

                            else:
                                if elem[elem.index('$') - 1] == '\\':
                                    content.append(elem.replace('\\$', '$'))
                                else:
                                    if elem[elem.index('$') + 1] == '{':
                                        var = elem[
                                            elem.index('{') + 1 : elem.index('}')
                                        ]
                                        elem = elem.replace(
                                            f'${{{var}}}',
                                            current.root.get_var(var),
                                        )
                                    else:
                                        var = elem[elem.index('$') + 1 :]
                                        elem = elem.replace(
                                            f'${var}', current.root.get_var(var)
                                        )
                                    content.append(elem)
                        content = ' '.join(content)

                    ind += 1
                case _:
                    return "Invalid syntax, use 'help open' for more information"
            ind += 1
        try:
            match mode:
                case 'r':
                    ans = '\n'.join(target.read(begin, end))
                case 'w':
                    target.write(content)
                case 'a':
                    target.append(content)
                case 'e':
                    target.edit(line, content)
                case 'i':
                    target.insert(line, content)
                case 'd':
                    target.delete(line)
                case _:
                    ans = Error(-2)
                    ans.add_description('Unknow mode')
        except IndexError:
            ans = Error(-2)
            ans.add_description("Given field is out of range")
        return ans