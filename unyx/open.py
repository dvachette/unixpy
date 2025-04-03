from .fs import File


def open_(current, args):
    r"""
    parsing the open command
    open -m <mode> -b <begin_line> [[-e <end_line>] [-c <content>]] [-l <line>] <path>

    the content can be multiline, just use \n to separate the lines

    modes:

    r: read
    open -m r -b <begin_line> -e <end_line> <path>

    w: write
    open -m w -c <content> <path>

    a: append
    open -m a -c <content> <path>

    e: edit
    open -m e -l <line> -c <content> <path>

    i: insert
    open -m i -l <line> -c <content> <path>

    d: delete
    open -m d -l <line> <path>
    """

    if len(args) < 1:
        return "Invalid syntax, use 'help open' for more information"

    target: File = current.find(args[-1])

    if target == -1:
        return 'No such file or directory'

    mode = None
    begin = 0
    end = None
    line = None
    content = None
    ind = 0

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
                    line = int(args[ind + 1])
                except IndexError:
                    return 'Missing param after -l'
                except ValueError:
                    return 'Invalid value for -l, must be an integer'
                ind += 1
            case '-c':
                try:
                    content = args[ind + 1]
                except IndexError:
                    return 'Missing param after -c'
                else:
                    content = content.split(' ')
                    ans = list()
                    for elem in content:
                        if '$' not in elem:
                            ans.append(elem)

                        else:
                            if elem[elem.index('$') - 1] == '\\':
                                ans.append(elem.replace('\\$', '$'))
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
                                ans.append(elem)
                    content = ' '.join(ans)

                ind += 1
            case _:
                return "Invalid syntax, use 'help open' for more information"
        ind += 1

    match mode:
        case 'r':
            return '\n'.join(target.read(begin, end))
        case 'w':
            target.write(content)
            return 'done'
        case 'a':
            target.append(content)
            return 'done'
        case 'e':
            target.edit(line, content)
            return 'done'
        case 'i':
            target.insert(line, content)
            return 'done'
        case 'd':
            target.delete(line)
            return 'done'
        case _:
            return "Invalid mode, use 'help open' for more information"
