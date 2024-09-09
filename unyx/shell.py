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
        display(f'Welcome to Unyx - {self.system_path}')
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
        }


    def run(self):
        running = True
        while running:
            try:
                command, *args = input(f'{self.current.path} # ').split(' ')
            except EOFError:
                break
            except KeyboardInterrupt:
                display("use 'exit' or <ctrl+z> to quit")
            command = command.lower()
            command = self.allias(command)
            args = [arg for arg in args if arg != '']
            match command:
                case 'exit':
                    running = False
                case 'ls':
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
                    for item in target:
                        if isinstance(item, Directory):
                            if item.name.startswith('.'):
                                if flag:
                                    display(f'{item.name}/')
                            else:
                                display(f'{item.name}/')
                        else:
                            if item.name.startswith('.'):
                                if flag:
                                    display(item.name)
                            else:
                                display(item.name)
                case 'cd':
                    self.current = self.current.find(args[0])

                case 'mkdir':
                    flag = True
                    for item in self.current:
                        if item.name == args[0]:
                            display('Directory already exists')
                            flag = False
                    valid_regex = r'^[^/\\:*?"<>|\s]+$'
                    if re.match(valid_regex, args[0]):
                        if not all([char == '.' for char in args[0]]) and flag:
                            Directory(self.current, args[0])
                        else:
                            display('Invalid directory name')
                    else:
                        display('Invalid directory name')
                case 'touch':
                    exists = False
                    for item in self.current:
                        if item.name == args[0]:
                            display('File already exists')
                            exists = True
                    valid_regex = r'^[^/\\:*?"<>|]+$'
                    if re.match(valid_regex, args[0]) and not exists:
                        File(self.current, args[0])
                    elif exists:
                        display('File already exists')
                    else:
                        display('Invalid file name')
                case 'rm':
                    flag = False
                    if args and args[0].lower() in ['-f','-force']:
                        flag = True
                        args.pop(0)
                    target = self.current.find(args[0])
                    if target == self.current:
                        display('Cannot delete current directory')
                    elif target == 'No such file or directory':
                        display(target)
                    else:
                        if isinstance(target, Directory) and len(target):
                            if self.current.descend_from(target):
                                display('Cannot delete current or parent directory')
                            else:
                                if flag:
                                    self.current.child.remove(target)
                                else:
                                    display(
                                        'Directory not empty, use rm -f <directory> to force delete'
                                    )
                        else:
                            self.current.child.remove(target)
                
                case 'help':
                    if args:
                        req = args[0]
                    else:
                        req = str()

                    doc = getattr(man, f'help_{req}')
                    display(doc())
                case 'open':
                    display(
                        open_(
                            current=self.current,
                            args=args,
                        )
                    )
                case 'var':
                    if args:
                        if args[0] == 'list':
                            display('\n'.join(self.current.root.vars.keys()))
                        elif len(args) >= 2:
                            match args[0]:
                                case 'set':
                                    self.current.root.vars[args[1]] = ' '.join(
                                        args[2:]
                                    )
                                case 'get':
                                    display(self.current.root.get_var(args[1]))
                                case 'del':
                                    self.current.root.remove_var(args[1])

                case 'mv':
                    ok = True
                    target = self.current.find(args[0])
                    dest = self.current.find(args[1])
                    if target == 'No such file or directory':
                        display('Source not found')
                        ok = False
                    if dest == 'No such file or directory':
                        display('Destination not found')
                        ok = False
                    for item in dest.child:
                        if item.name == target.name:
                            display('File already exists')
                            ok = False
                    if ok:
                        target.move(dest)

                case 'cp':
                    target = self.current.find(args[0])
                    if '/' in args[1]:
                        dest, name = args[1].rsplit('/', 1)
                    else:
                        dest, name = '.', args[1]
                    
                    copy = target.copy()
                    copy.rename(name)
                    copy.move(self.current.find(dest))

                case '':
                    pass

                case 'rename':
                    target = self.current.find(args[0])
                    target.rename(args[1])
                case _:
                    display(
                        'Unknow command',
                        'Use "help" to see all available commands',
                        sep='\n',
                    )

            with open(self.system_path, 'wb') as f:
                pickle.dump(self.system, f)
            with open(self.log_file, 'a') as f:
                f.write(f'{self.current.path}# {command} {" ".join(args)}\n')
    def allias(self,value):
        for command, alliasses in self.alliasses.items():
            if value in alliasses:
                return command
        return value

display = print
