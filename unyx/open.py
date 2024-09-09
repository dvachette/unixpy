from .unixsys import File


def open_(current, args):
    r"""
    parsing the open command
    open <path> <mode> <*args>

    the content can be multiline, just use \n to separate the lines

    modes:

    r: read
    open <path> -r [start[end]]

    w: write
    open <path> -w <content>

    a: append
    open <path> -a <content>

    e: edit
    open <path> -e <line> <content>

    i: insert
    open <path> -i <line> <content>

    d: delete
    open <path> -d <line>
    """

    target: File = current.find(args[0])
    if target == 'No such file or directory':
        return target
    if len(args) < 2:
        mode = '-r'
    else:
        mode = args[1]
    match mode:
        case '-r':
            start = 0
            end = None
            if len(args) >= 3:
                start = int(args[2])
            if len(args) >= 4:
                end = int(args[3])
            return '\n'.join(target.read(start, end))
        case '-w':
            content = args[2:]
            target.write(content)
            return 'done'
        case '-a':
            content = args[2:]
            target.append(content)
            return 'done'
        case '-e':
            line = int(args[2])
            content = args[3]
            target.edit(line, content)
            return 'done'
        case '-i':
            line = int(args[2])
            content = args[3]
            target.insert(line, content)
            return 'done'
        case '-d':
            line = int(args[2])
            target.delete(line)
            return 'done'
        case _:
            return "Invalid mode, use 'help open' for more information"
