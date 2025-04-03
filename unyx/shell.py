from __future__ import annotations

import pickle
import re

from .fs import Directory, File, Root, __ContainerFSObject
from . import man
from .open import open_
from .unyxutils import notImplementedYet
from .errors import Error


class Shell:
    def __init__(self, instance_path: str):
        self.running: bool = False
        self.system_path: str = instance_path
        with open(self.system_path, 'rb') as f:
            self.file_system: Root = pickle.load(f)
        self.current: __ContainerFSObject = self.file_system
        self.root: Root = self.file_system
        self.log_file_path: str = self.system_path + '.history'
        self.output(f'Welcome to Unyx - {self.system_path}')
        self.alliasses: dict[str : list[str]] = {
            'ls': ['list', 'ls', 'dir'],
            'cd': ['chdir', 'cd'],
            'mkdir': ['md', 'mkdir'],
            'touch': ['new', 'touch'],
            'rm': ['delete', 'rm', 'del', 'remove'],
            'exit': ['quit', 'exit'],
            'help': ['?', 'help'],
            'open': ['open'],
            'cp': ['copy', 'cp'],
            'mv': ['move', 'mv'],
            'rename': ['ren', 'rn', 'rename'],
            'var': ['var'],
            'echo': ['echo'],
            'cat': ['cat'],
            'cut': ['cut'],
            'grep': ['grep'],
            'sudo': ['sudo'],
        }

    def run(self):
        self.running = True
        while self.running:
            try:
                entered: str = input(f'{self.current.path} # ')

                # do not space split arguments in quotes
                args: list[str] = re.findall(r'(?:"[^"]*"|[^\s"])+', entered)
                # Separate the command from the arguments
                command = args[0]
                args = args[1:]
                args = [arg.replace('"', '') for arg in args]

            except EOFError:
                break   # Exiting repl
            except KeyboardInterrupt:
                self.output("Use 'exit' or <ctrl+z> to quit")
                continue

            args = list(
                filter(lambda s: s != '', args)
            )   # remove empty strings created by multiple spaces

            # Manage output redirection
            filename_output: str | None = (
                None  # default destination for output redirection
            )
            mode = 'w'   # default mode for output redirection

            if (
                args and len(args) >= 2 and args[-2] == '>'
            ):   # if output redirection is used with '>'
                filename_output = args[-1]   # get the filename
                args = args[
                    :-2
                ]   # remove the redirection part from the arguments
                mode = 'w'   # set the mode to write
            if (
                args and len(args) >= 2 and args[-2] == '>>'
            ):   # if output redirection is used with '>>'
                filename_output = args[-1]   # get the filename
                args = args[
                    :-2
                ]   # remove the redirection part from the arguments
                mode = 'a'   # set the mode to append

            command = command.lower()   # make the command case insensitive
            command = self.allias(command)   # check if the command is an alias
            if '|' in args:   # if pipe is used
                ans = self.pipe(command, args)   # create the ans using a pipe
            else:
                ans = self.execute(
                    command, *args
                )   # create the ans using the standard method
            self.output(
                ans, filename_output, mode
            )   # output the ans to the console or to a file

            with open(
                self.system_path, 'wb'
            ) as f:   # save the system to the file
                pickle.dump(self.file_system, f)

            with open(self.log_file_path, 'a') as f:   # log the command
                f.write(f'{self.current.path} # {command} {" ".join(args)}\n')

    def allias(self, value):

        for command, alliasses in self.alliasses.items():
            if value in alliasses:
                return command
        return value

    def execute(self, command, *args):
        ans = str()
        match command:
            case 'sudo':
                pass
            case 'exit':
                self.running = False
            case 'ls':
                ans = self.ls(*args)
            case 'cd':
                ans = self.cd(*args)
            case 'mkdir':
                ans = self.mkdir(*args)
            case 'touch':
                ans = self.touch(*args)
            case 'rm':
                ans = self.rm(*args)
            case 'help':
                ans = self.help(*args)
            case 'cat':
                ans = open_(
                    current=self.current,
                    args=('-m', 'r', args[-1]),
                )
            case 'open':
                ans = open_(
                    current=self.current,
                    args=args,
                )
            case 'var':
                ans = self.var(*args)
            case 'mv':
                ans = self.mv(*args)
            case 'cp':
                ans = self.cp(*args)
            case '':
                ans = ''
            case 'rename':
                ans = self.rename(*args)
            case 'echo':
                ans = self.echo(*args)
            case 'cut':
                ans = self.cut(*args)
            case 'grep':
                ans = self.grep(*args)
            case _:
                ans = """\
                    Unknow command
                    Use "help" to see all available commands
                """
        if not ans:
            ans = ''
        return ans

    def pipe(self, command, args):
        args = (command, *args)
        commands = list()
        part: list = list()
        for arg in args:
            if arg != '|':
                part.append(arg)
            else:
                commands.append(part)
                part = list()
        commands.append(part)   # append the last part
        file_ans = None
        for command in commands:
            if file_ans is None:
                txt_ans = self.execute(command[0], *command[1:])
                if isinstance(txt_ans, Error):
                    return txt_ans
                file_ans = File(self.root.find('tmp'), 'tmp_file')
                file_ans.write(txt_ans)
            else:
                txt_ans = self.execute(command[0], *command[1:], file_ans.path)
                if isinstance(txt_ans, Error):
                    return txt_ans
                file_ans.write(txt_ans)
        ans = txt_ans
        self.rm(file_ans.path)
        return ans

    def cd(self, *args):
        if args:
            target = self.current.find(args[0])
        else:
            return self.current.path
        if isinstance(target, Error):
            return target
        elif isinstance(target, File):
            ans = Error(-5)
            ans.add_description('Not a directory')
            return ans
        else:
            self.current = target

    def grep(self, *args):
        filepath = args[-1]
        file: File | Error = self.current.find(filepath)
        if isinstance(file, Error):
            return file
        args = args[:-1]
        return file.grep(*args)

    def ls(self, *args):
        target = self.current
        flag = False

        if args and args[0] == '-a':
            args = list(args)
            flag = True
            args.pop(0)
        if args:
            paths_regex = r'(^/|^\.{1,2}/|^[^/])([^/\0]+/)*([^/\0]+)?'
            if re.match(paths_regex, args[0]):
                target = self.current.find(args[0])
        ans = list()
        for item in target:
            if isinstance(item, Directory):
                if item.name.startswith('.'):
                    if flag:
                        ans.append(f'{item.name}/')
                else:
                    ans.append(f'{item.name}/')
            else:
                if item.name.startswith('.'):
                    if flag:
                        ans.append(item.name)
                else:
                    ans.append(item.name)
        return '\n'.join(ans)

    def rm(self, *args):
        args = list(args)
        flag = False
        if args and args[0].lower() in ['-f', '-force']:
            flag = True
            args.pop(0)
        target = self.current.find(args[0])
        if target == self.current:
            ans = Error(-5)
            ans.add_description('Cannot delete current directory')
            return ans
        elif isinstance(target, Error):
            return target
        else:
            if isinstance(target, Directory) and len(target):
                if self.current.descend_from(target):
                    return 'Cannot delete current or parent directory'
                else:
                    if flag:
                        target.parent.child.remove(target)
                    else:
                        ans = Error(-5)
                        ans.add_description(
                            'Directory not empty, use rm -f <directory> to force delete'
                        )
                        return ans
            else:
                target.parent.child.remove(target)

    def touch(self, *args):
        for item in self.current:
            if item.name == args[0]:
                return 'File already exists'
        valid_regex = r'^[^/\\:*?"<>|]+$'
        if re.match(valid_regex, args[0]):
            File(self.current, args[0])
        else:
            ans = Error(-2)
            ans.add_description('Invalid file name')
            return ans

    def help(self, *args):
        if args:
            req = args[0]
        else:
            req = str()
        try:
            doc = getattr(man, f'help_{req.lower()}')
        except AttributeError:
            ans = Error(-4)
            ans.add_description('No such command')
            return ans
        else:
            return doc()

    def exit(self):
        self.running = False
        return 'Shell closed'

    def rename(self, args):
        target = self.current.find(args[0])
        name = args[1]
        name_regex = r'^[^/\\:*?"<>|]+$'
        if not re.match(name_regex, name):
            ans = Error(-2)
            ans.add_description('Invalid name')
            return ans
        if isinstance(target, Error):
            return target
        target.rename(args[1])

    def cp(self, args):
        target = self.current.find(args[0])
        if isinstance(Error):
            return target
        if '/' in args[1]:
            dest, name = args[1].rsplit('/', 1)
        else:
            dest, name = '.', args[1]
        name_regex = r'^[^/\\:*?"<>|]+$'
        if not re.match(name_regex, name):
            ans = Error(-2)
            ans.add_description('Invalid name')
            return ans
        dest = self.current.find(dest)
        if isinstance(target, Error):
            return target
        copy = target.copy()
        copy.rename(name)
        copy.move(dest)

    def mv(self, args):
        target = self.current.find(args[0])
        dest = self.current.find(args[1])
        if isinstance(target, Error):
            target.add_description('Invalid target')
            return target
        if isinstance(dest, Error):
            dest.add_description('Destination not found')
            return dest
        for item in dest.child:
            if item.name == target.name:
                ans = Error(-2)
                ans.add_description('File already exists')
                return ans
        target.move(dest)

    def var(self, *args):
        if args:
            if args[0] == 'list':
                return '\n'.join(self.current.root.vars.keys())
            elif args[0] == 'dict':
                return '\n'.join(
                    [f'{key}={value}' for key, value in self.current.root.vars]
                )
            elif len(args) >= 2:
                match args[0]:
                    case 'set':
                        self.current.root.vars[args[1]] = ' '.join(args[2:])
                    case 'get':
                        return self.current.root.get_var(args[1])
                    case 'del':
                        self.current.root.remove_var(args[1])

    def mkdir(self, *args):
        for item in self.current:
            if item.name == args[0]:
                ans = Error(-2)
                ans.add_description('Directory already exists')
                return ans
        valid_regex = r'^[^/\\:*?"<>|\s]+$'
        if re.match(valid_regex, args[0]):
            if not all([char == '.' for char in args[0]]):
                Directory(self.current, args[0])
            else:
                ans = Error(-2)
                ans.add_description('Invalid directory name')
                return ans
        else:
            ans = Error(-2)
            ans.add_description('Invalid directory name')
            return ans

    def echo(self, *args: str):
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
                            f'${{{var}}}', self.current.root.get_var(var)
                        )
                    else:
                        var = arg[arg.index('$') + 1 :]
                        arg = arg.replace(
                            f'${var}', self.current.root.get_var(var)
                        )
                    ans.append(arg)
        return ' '.join(ans)

    def cut(self, *args):
        if len(args) < 4:
            ans = Error(-3)
            ans.add_description('Missing arguments')
            return ans
        filepath = args[-1]
        file: File = self.current.find(filepath)
        if isinstance(file, Error):
            return file

        sep = None
        fields = None

        i = 0
        l = len(args)
        while i < l:
            if args[i] == '-d':
                sep = args[i + 1]
                i += 2
            elif args[i] == '-f':
                fields = args[i + 1]
                i += 2
            else:
                i += 1
        if sep is None or fields is None:
            ans = Error(-3)
            ans.add_description('Missing either -d or -f option')
            return ans

        ans = file.cut(sep, fields)
        return ans

    def output(self, value, filename=None, type_: str = 'w'):
        if filename is None:
            if value == '':
                return
            print(value)
        else:
            file: File | Error = self.current.find(filename)
            if isinstance(file, Error):
                ans = self.touch(filename)
                if isinstance(ans, Error):
                    ans.add_description('On redirect, Invalid filename')
                    print(ans)

            if isinstance(file, Directory):
                ans = Error(-2)
                ans.add_description('Cannot write inside of a directory')
                print(ans)
            file: File = self.current.find(filename)
            if type_ == 'w':
                file.write(value)
            elif type_ == 'a':
                file.append(value)
