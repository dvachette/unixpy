from .unixsys import Directory, File, Root
import pickle
import re
from . import man
from .open import open_


class Shell:
    def __init__(self, system: str):
        self.system_path = system
        with open(self.system_path, 'rb') as f:
            self.system: Root = pickle.load(f)
        self.current = self.system
        self.root = self.system
        self.log_file = self.system_path + '.history'
        self.output(f'Welcome to Unyx - {self.system_path}')
        self.alliasses = {
            'ls': ['list','ls','dir'],
            'cd': ['chdir','cd'],
            'mkdir': ['md','mkdir'],
            'touch': ['new','touch'],
            'rm': ['delete','rm','del','remove'],
            'exit': ['quit','exit'],
            'help': ['?', 'help'],
            'open': ['open'],
            'cp': ['copy','cp'],
            'mv': ['move','mv'],
            'rename': ['ren','rn','rename'],
            'var': ['var'],
            'echo': ['echo'],
            'cat': ['cat'],
            'cut': ['cut'],
            'grep': ['grep']
        }


    def run(self):
        self.running = True
        while self.running:
            try:
                # do not space split arguments in quotes

                entered = input(f'{self.current.path} # ')
                args = re.findall(r'(?:"[^"]*"|[^\s"])+', entered)
                command = args[0]
                args = args[1:]
                args = [arg.replace('"', '') for arg in args]

                
            except EOFError:
                break
            except KeyboardInterrupt:
                self.output(" Use 'exit' or <ctrl+z> to quit")
                continue
            command = command.lower()
            command = self.allias(command)
            filename_output = None
            mode = 'w'
            args = [arg for arg in args if arg != '']
            if args and len(args) >= 2 and args[-2] == '>':
                filename_output = args[-1]
                args = args[:-2]
                mode = 'w'
            if args and len(args) >= 2 and args[-2] == '>>':
                filename_output = args[-1]
                args = args[:-2]
                mode = 'a'
            ans = self.execute(command,*args)
            self.output(ans, filename_output, mode)
            with open(self.system_path, 'wb') as f:
                pickle.dump(self.system, f)
            with open(self.log_file, 'a') as f:
                f.write(f'{self.current.path} # {command} {" ".join(args)}\n')

                
    def allias(self,value):
        for command, alliasses in self.alliasses.items():
            if value in alliasses:
                return command
        return value


    def execute(self, command, *args):
        ans = str()
        match command:
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
            ans = ""
        return ans
            
    def cd(self, *args):
        if args:
            target = self.current.find(args[0])
        else:
            return self.current.path
        if target == 'No such file or directory':
            return target
        elif isinstance(target, File):
            return 'Not a directory'
        else:
            self.current = target

    def grep(self, *args):
        filepath = args[-1]
        file:File = self.current.find(filepath)
        if file == 'No such file or directory':
            return file
        args = args[:-1]
        return file.grep(*args)

    def ls(self, *args):
        target = self.current
        flag = False
        if args and args[0] == '-a':
            flag = True
            args.pop(0)
        if args:
            paths_regex = (
                r'(^/|^\.{1,2}/|^[^/])([^/\0]+/)*([^/\0]+)?'
            )
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
        flag = False
        if args and args[0].lower() in ['-f','-force']:
            flag = True
            args.pop(0)
        target = self.current.find(args[0])
        if target == self.current:
            return 'Cannot delete current directory'
        elif target == 'No such file or directory':
            return target
        else:
            if isinstance(target, Directory) and len(target):
                if self.current.descend_from(target):
                    return 'Cannot delete current or parent directory'
                else:
                    if flag:
                        self.current.child.remove(target)
                    else:
                        return 'Directory not empty, use rm -f <directory> to force delete'
            else:
                self.current.child.remove(target)
    def touch(self, *args):
        for item in self.current:
            if item.name == args[0]:
                return 'File already exists'
        valid_regex = r'^[^/\\:*?"<>|]+$'
        if re.match(valid_regex, args[0]):
            File(self.current, args[0])
        else:
            return 'Invalid file name'
    def help(self, *args):
        if args:
            req = args[0]
        else:
            req = str()

        doc = getattr(man, f'help_{req}')
        return doc()

    def exit(self):
        self.running = False
        return 'Shell closed'
    
    def rename(self, args):
        target = self.current.find(args[0])
        name = args[1]
        name_regex  = r'^[^/\\:*?"<>|]+$'
        if not re.match(name_regex, name):
            return 'Invalid name'
        if target == 'No such file or directory':
            return target
        target.rename(args[1])

    def cp(self, args):
        target = self.current.find(args[0])
        if target == 'Invalid source':
            return target
        if '/' in args[1]:
            dest, name = args[1].rsplit('/', 1)
        else:
            dest, name = '.', args[1]
        name_regex  = r'^[^/\\:*?"<>|]+$'
        if not re.match(name_regex, name):
            return 'Invalid name'
        dest = self.current.find(dest)
        if dest == 'No such file or directory':
            return 'Invalid destination'
        copy = target.copy()
        copy.rename(name)
        copy.move(dest)
    
    def mv(self, args):
        target = self.current.find(args[0])
        dest = self.current.find(args[1])
        if target == 'No such file or directory':
            return 'Source not found'
        if dest == 'No such file or directory':
            return 'Destination not found'
        for item in dest.child:
            if item.name == target.name:
                return 'File already exists'
        target.move(dest)
    
    def var(self, *args):
        if args:
            if args[0] == 'list':
                return '\n'.join(self.current.root.vars.keys())
            elif len(args) >= 2:
                match args[0]:
                    case 'set':
                        self.current.root.vars[args[1]] = ' '.join(
                            args[2:]
                        )
                    case 'get':
                        return self.current.root.get_var(args[1])
                    case 'del':
                        self.current.root.remove_var(args[1])

    def mkdir(self, *args):
        flag = True
        for item in self.current:
            if item.name == args[0]:
                return 'Directory already exists'
                flag = False
        valid_regex = r'^[^/\\:*?"<>|\s]+$'
        if re.match(valid_regex, args[0]):
            if not all([char == '.' for char in args[0]]) and flag:
                Directory(self.current, args[0])
            else:
                return 'Invalid directory name'
        else:
            return 'Invalid directory name'


    def echo(self, *args: str):
        ans = list()
        for arg in args:
            if "$" not in arg:
                ans.append(arg)
            else:
                if arg[arg.index("$")-1] == "\\":
                    ans.append(arg.replace("\\$", "$"))
                else:
                    if arg[arg.index("$")+1] == "{":
                        var = arg[arg.index("{")+1:arg.index("}")]
                        arg = arg.replace(f'${{{var}}}', self.current.root.get_var(var))
                    else:
                        var = arg[arg.index("$")+1:]
                        arg = arg.replace(f'${var}', self.current.root.get_var(var))
                    ans.append(arg)
        return ' '.join(ans)

    def cut(self, *args):
        filepath = args[-1]
        file:File = self.current.find(filepath)
        if file == 'No such file or directory':
            return file

        sep = None
        fields = None

        i = 0
        l = len(args)
        while i < l:
            if args[i] == '-d':
                sep = args[i+1]
                i += 2
            elif args[i] == '-f':
                fields = args[i+1]
                i += 2
            else:
                i += 1
        if sep is None or fields is None:
            return 'Invalid arguments'
        
        ans = file.cut(sep, fields)
        return ans

    def output(self, value, filename=None, type_:str='w'):
        if filename is None:
            if value == "":
                return
            print(value)
        else:
            file:File = self.current.find(filename)
            if file == 'No such file or directory':
                ans = self.touch(filename)
                if ans == 'Invalid file name':
                    print(ans)
            file:File = self.current.find(filename)
            if type_ == 'w':
                file.write(value)
            elif type_ == 'a':
                file.append(value)

