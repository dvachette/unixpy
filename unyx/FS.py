from __future__ import annotations

from typing import Callable, Literal 
import pickle
import re
from .commands import ls, rm, touch, cd, grep, rename, cp, mv, var, mkdir, echo, cut, open_
from ._fs import Directory, File, Root, _ContainerFSObject
from . import man
from .unyxutils import notImplementedYet
from .errors import Error


class FS:
    def __init__(self, instance_path: str):
        assert isinstance(instance_path, str), 'instance_path must be a string'
        self.running: bool = False
        self.system_path: str = instance_path
        try:
            with open(self.system_path, 'rb') as f:
                self.file_system: Root = pickle.load(f)
        except FileNotFoundError:
            # Create the root directory if the file does not exist
            self.output(f'File {self.system_path} not found. Creating a new instance file')
            self.file_system: Root = Root()
            self.current = self.file_system
            self._mkdir('tmp')
        except EOFError:
            raise Exception("File is empty")
        except pickle.UnpicklingError:
            raise Exception("File is corrupted")
        except Exception as e:
            raise Exception(f"Unknown error: {e}")
        
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
            'pwd': self._pwd,
            'ls': self._ls,
            'cd': self._cd,
            'mkdir': self._mkdir,
            'touch': self._touch,
            'rm': self._rm,
            'help': self._help,
            'open': self._open,
            'var': self._var,
            'mv': self._mv,
            'cp': self._cp,
            'rename': self._rename,
            'echo': self._echo,
            'cut': self._cut,
            'grep': self._grep,
            'sudo': self._sudo,
            'cat': self._cat,
            'exit': self._exit,
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
            filename_output: str | None = None  # default destination for output redirection
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

            self.save()
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

    def _cat(self, *args):
        ans = open_(self, *('-m', 'r', args[-1]))
        self.save()
        return ans

    def _ls(self, *args):
        ans = ls(self, *args)
        self.save()
        return ans

    def _cd(self, *args):
        ans = cd(self, *args)
        self.save()
        return ans
    
    def _mkdir(self, *args):
        ans = mkdir(self, *args)
        self.save()
        return ans
    
    def _touch(self, *args):
        ans = touch(self, *args)
        self.save()
        return ans  
    
    def _rm(self, *args):
        ans = rm(self, *args)
        self.save()
        return ans
    
    def _open(self, *args):
        ans = open_(self, *args)
        self.save()
        return ans
    
    def _var(self, *args):
        ans = var(self, *args)
        self.save()
        return ans
    
    def _mv(self, *args):
        ans = mv(self, *args)
        self.save()
        return ans
    
    def _cp(self, *args):
        ans = cp(self, *args)
        self.save()
        return ans
    
    def _rename(self, *args):
        ans = rename(self, *args)
        self.save()
        return ans
    
    def _echo(self, *args):
        ans = echo(self, *args)
        self.save()
        return ans
    
    def _cut(self, *args):
        ans = cut(self, *args)
        self.save()
        return ans
    
    def _grep(self, *args):
        ans = grep(self, *args)
        self.save()
        return ans
    
    def _pwd(self, *args):
        return self.current.path

    @notImplementedYet
    def _sudo(self, *args):
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
        self._rm(file_ans.path)
        return ans

    def _help(self, *args):
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

    def _exit(self, *args):
        # . *args is not used but is required to match the function signature of the REPL method
        self.running = False
        return 'REPL closed'

    def readfile(self, filepath:str) -> str | Error:
        return self._cat(filepath)

    def listdir(self, dirpath=None) -> list[str] | Error:
        if dirpath is None:
            return self._ls().split('\n')
        return self._ls(dirpath).split('\n')
    
    def chdir(self, dirpath:str) -> None | Error:
        return self._cd(dirpath)
    
    def makedir(self, dirname:str) -> None | Error:
        return self._mkdir(dirname)

    def makefile(self, filename:str) -> None | Error:
        return self._touch(filename)

    def rmdir(self, dirpath:str) -> None | Error:
        return self._rm("-f", dirpath)

    def removefile(self, filename:str) -> None | Error:
        return self._rm(filename)
    
    def open(self, filename:str, mode:Literal['a', 'e', 'r', 'w', 'i', 'd']=None, content:str=None, line:int=None, begin:int=None, end:int=None) -> str | Error:
        if mode is None:
            return self._cat(filename)
        args = ['-m', mode]
        if content is not None:
            args.extend(['-c', content])
        if line is not None:
            args.extend(['-l', line])
        if begin is not None:
            args.extend(['-b', begin])
        if end is not None:
            args.extend(['-e', end])
        args.append(filename)
        if mode in 'waei' and content is None:
            raise ValueError('Content is required for write, append, edit and insert modes')
        return self._open(*tuple(args))

    def writeinfile(self, filename:str, content:str) -> None | Error:
        return self._open('-m', 'w', '-c', content, filename)
    
    def appendinfile(self, filename:str, content:str) -> None | Error:
        return self._open('-m', 'a', '-c', content, filename)
    
    def editinfile(self, filename:str, content:str, line:int) -> None | Error:
        return self._open('-m', 'e', '-c', content, '-l', str(line), filename)
    
    def insertinfile(self, filename:str, content:str, line:int) -> None | Error:
        return self._open('-m', 'i', '-c', content, '-l', str(line), filename)
    
    def deleteinfile(self, filename:str, line:int) -> None | Error:
        return self._open('-m', 'd', '-l', str(line), filename)
    
    def readinfile(self, filename:str, begin:int=None, end:int=None) -> str | Error:
        args = list()
        if begin is not None:
            args.extend(['-b', str(begin)])
        if end is not None:
            args.extend(['-e', end])

        args.append(filename)

        return self._open(*args)

    def getvar(self, varname:str) -> str | Error:
        return self._var('get', varname)
    
    def setvar(self, varname:str, value:str) -> None | Error:
        return self._var('set', varname, value)
    
    def getvarlist(self) -> list[str] | Error:
        return self._var('list').split('\n')

    def getvardict(self) -> dict[str, str] | Error:
        ans = self._var('list')
        if isinstance(ans, Error):
            return ans
        else:
            ans = ans.split('\n')
            ans = [line.split('=') for line in ans]
            return dict(ans)
        
    def delvar(self, varname:str) -> None | Error:
        return self._var('del', varname)
    
    def move(self, src:str, dest:str) -> None | Error:
        return self._mv(src, dest)
    
    def copy(self, src:str, dest:str) -> None | Error:
        return self._cp(src, dest)
    
    def rename(self, src:str, dest:str) -> None | Error:
        return self._rename(src, dest)
    
    def grep(self, pattern:str, filename:str) -> str | Error:
        return self._grep(pattern, filename)
    
    def cut(self, filename:str, separator:str, fields:str) -> str | Error:
        return self._cut(filename, separator, fields)
    
    def echo(self, *args) -> str | Error:
        return self._echo(*args)

    def getcwd(self):
        return self._pwd()

    def output(self, value:str|Error, filename=None, type_: Literal['w','a'] = 'w'):
        if filename is None:
            if value == '':
                return
            print(value)
        else:
            file: File | Error = self.current.find(filename)
            if isinstance(file, Error):
                ans = self._touch(filename)
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

    def save(self):
        with open(self.system_path, 'wb') as f:
            pickle.dump(self.file_system, f)