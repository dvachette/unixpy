from .unixsys import Directory, File, Root
import pickle
import re
from . import man


class Shell:
    def __init__(self, system:str):
        self.system_path = system
        with open(self.system_path, 'rb') as f:
            self.system:Root = pickle.load(f)
        self.current = self.system
        self.root = self.system
        self.log_file = self.system_path.split(".")[0]+".txt"


    def run(self):
        running = True
        while running:
            try:
                command, *args = input(f'{self.current.path}# ').split(' ')
            except EOFError:
                break
            match command:
                case 'exit':
                    running = False
                case 'ls':
                    target = self.current
                    if args:
                        paths_regex = r'(^/|^\.{1,2}/|^[^/])([^/\0]+/)*([^/\0]+)?'
                        if re.match(paths_regex,args[0]):
                            target = self.current.find(args[0])
                    for item in target:
                        if isinstance(item, Directory):
                            display(f'{item.name}/')
                        else:
                            display(item.name)
                case 'cd':
                    self.current = self.current.find(args[0])
                
                case "mkdir":
                    valid_regex = r'^[^/\\:*?"<>|]+$'
                    if re.match( valid_regex, args[0]):
                        Directory(self.current, args[0])
                    else:
                        display('Invalid directory name')
                case "touch":
                    valid_regex = r'^[^/\\:*?"<>|]+$'
                    if re.match(valid_regex,args[0]):
                        File(self.current, args[0])
                    else:
                        display('Invalid file name')
                case "rm":
                    target = self.current.find(args[0])
                    if target == self.current:
                        display('Cannot delete current directory')
                    elif target == "No such file or directory":
                        display(target)
                    else:
                        if isinstance(target, Directory) and len(target) > 0:
                            if len(args) >= 2 and args[1].lower() == "-f":
                                self.current.child.remove(target)
                            else:
                                display('Directory not empty, use -f to force delete')
                        else:
                            self.current.child.remove(target)
                case "help":
                    if args:
                        req = args[0]
                    else:
                        req = str()
                    
                    doc = getattr(man, f'help_{req}')
                    display(doc())
            with open(self.system_path, 'wb') as f:
                pickle.dump(self.system, f)
            with open(self.log_file, 'a') as f:
                f.write(f'{self.current.path}# {command} {" ".join(args)}\n')
display = print