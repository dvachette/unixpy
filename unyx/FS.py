from __future__ import annotations

import pickle
import re
from .commands import ls, rm, touch, cd, grep, rename, cp, mv, var, mkdir, echo, cut
from ._fs import Directory, File, Root, _ContainerFSObject
from . import man
from .open import open_
from .unyxutils import notImplementedYet
from .errors import Error


class FS:
    def __init__(self, instance_path: str):
        assert isinstance(instance_path, str), 'instance_path must be a string'
        self.running: bool = False
        self.system_path: str = instance_path
        with open(self.system_path, 'rb') as f:
            self.file_system: Root = pickle.load(f)
        self.current: _ContainerFSObject = self.file_system
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
            'pwd': ['pwd'],
        }
        self.commands: dict[str : function] = {
            'pwd': self.pwd,
            'ls': self.ls,
            'cd': self.cd,
            'mkdir': self.mkdir,
            'touch': self.touch,
            'rm': self.rm,
            'help': self.help,
            'open': open_,
            'var': self.var,
            'mv': self.mv,
            'cp': self.cp,
            'rename': self.rename,
            'echo': self.echo,
            'cut': self.cut,
            'grep': self.grep,
            'sudo': self.sudo,
            'cat': self.cat,
            'exit': self.exit,
            '': lambda: '',
        }

    def REPL(self):
        self.running = True
        while self.running:
            try:
                entered: str = input(f'{self.current.path} # ')
            except EOFError:
                break   # Exiting repl
            except KeyboardInterrupt:
                self.output("\nUse 'exit' or <ctrl+D> to quit")
                continue
            ans = self.execute(entered)

            with open(self.log_file_path, 'a') as f:   # log the command
                f.write(f'{self.current.path} # {entered}\n')
                f.write(f'{ans}\n')

    def execute(self, command, show_output: bool = True):
                    
            args: list[str] = re.findall(r'(?:"[^"]*"|[^\s"])+', command)

            command = args[0]
            args = args[1:]
            args = [arg.replace('"', '') for arg in args]

            args = list(
                filter(lambda s: s != '', args)
            )   # remove empty strings created by multiple spaces

            # Manage output redirection
            filename_output: str | None = (
                None  # default destination for output redirection
            )
            mode = 'w' # default mode for output redirection

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
                ans:str|Error = self.runCommand(
                    command, *args
                )   # create the ans using the standard method
            if not show_output and filename_output is None:
                return ans
            self.output(
                ans, filename_output, mode
            )   # output the ans to the console or to a file

            with open(
                self.system_path, 'wb'
            ) as f:   # save the system to the file
                pickle.dump(self.file_system, f)
            return ans

    def allias(self, value):
        for command, alliasses in self.alliasses.items():
            if value in alliasses:
                return command
        return value

    def runCommand(self, command, *args):
        ans = str()
        ans = self.commands.get(command, lambda *args: """Unknow command\nUse "help" to see all available commands""")(*args)
        if not ans:
            ans = ''
        return ans

    def cat(self, *args):
        ans = open_(current=self.current, args=('-m', 'r', args[-1]))
        return ans

    def ls(self, *args):
        ans = ls(self, *args)
        return ans

    def cd(self, *args):
        ans = cd(self, *args)
        return ans
    
    def mkdir(self, *args):
        ans = mkdir(self, *args)
        return ans
    
    def touch(self, *args):
        ans = touch(self, *args)
        return ans  
    
    def rm(self, *args):
        ans = rm(self, *args)
        return ans
    
    def open(self, *args):
        ans = open_(current=self.current, args=args)
        return ans
    
    def var(self, *args):
        ans = var(self, *args)
        return ans
    
    def mv(self, *args):
        ans = mv(self, *args)
        return ans
    
    def cp(self, *args):
        ans = cp(self, *args)
        return ans
    
    def rename(self, *args):
        ans = rename(self, *args)
        return ans
    
    def echo(self, *args):
        ans = echo(self, *args)
        return ans
    
    def cut(self, *args):
        ans = cut(self, *args)
        return ans
    
    def grep(self, *args):
        ans = grep(self, *args)
        return ans
    
    def pwd(self, *args):
        return self.current.path()

    @notImplementedYet
    def sudo(self, *args):
        pass



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

    def exit(self, *args):
        # *args is not used but is required to match the function signature
        # of the REPL method
        self.running = False
        return 'Shell closed'

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
