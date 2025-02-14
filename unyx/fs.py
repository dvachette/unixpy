from __future__ import annotations

import re

from .unyxutils import notImplementedYet
from .errors import Error

class File:
    def __init__(self, parent, name):
        self.name = name
        self.parent:Directory|Root = parent
        self.data = list()
        if isinstance(parent, Root):
            self.root = self.parent
        else:
            self.root = self.parent.root
        self.parent.child.append(self)

    def __repr__(self):
        return f'File({self.parent},{self.name})'

    def __str__(self):
        return self.name

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data

    def descend_from(self, item):
        if item == self:
            return True
        if item == self.root:
            return True
        return self.descend_from(item.parent)
    
    def copy(self):
        new = File(self.parent, self.name)
        new.data = self.data.copy()
        return new

    @property
    def path(self):
        return self.parent.path + self.name

    def read(self, start=0, end=None, lines=False):
        if lines:
            if end is None:
                content = self.data[start:]
            content = self.data[start:end]
            ans = []
            for i , data in enumerate(content):
                ans.append(f'{i} {data}')
            return ans
        if end is None:
            return self.data[start:]
        return self.data[start:end]

    def write(self, content):
        self.data = content.split('\\n')

    def move(self, target):
        self.parent.child.remove(self)
        self.parent = target
        self.parent.child.append(self)

    def append(self, content):
        self.data.extend(content.split('\\n'))

    def insert(self, line, content):
        self.data.insert(line, content)

    def delete(self, line):
        del self.data[line]

    def edit(self, line, content):
        self.data[line] = content

    def find(self, path):
        return Error(-5)

    def rename(self, name):
        self.name = name

    def cut(self, separator, fields):
        l_fields = list()
        fields = fields.split(' ')
        for field in fields:
            if '-' not in field:
                if field.isdigit():
                    l_fields.append(int(field)-1)
                else:
                    ans = Error(-2)
                    ans.add_description('Invalid field')
                    return ans
            else:
                start, end = field.split('-')
                if start.isdigit() and end.isdigit():
                    l_fields.extend(range(int(start)-1, int(end)))
                else:
                    ans = Error(-2)
                    ans.add_description('Invalid field')
                    return ans
        ans = list()
        for line in self.data:
            linesplit = line.split(separator)
            ans.append(separator.join([linesplit[i] for i in l_fields]))
        return "\n".join(ans)


    def grep(self, pattern):
        ans = list()
        pattern = self.convert_grep_to_re(pattern)
        for line in self.data:
            if re.search(pattern, line):
                ans.append(line)
        return "\n".join(ans)
    
    def convert_grep_to_re(self, grep_pattern: str) -> str:
        # Remplacer les groupes de capture
        re_pattern = grep_pattern.replace(r'\(', '(').replace(r'\)', ')')
        # Remplacer les alternatives
        re_pattern = re_pattern.replace(r'\|', '|')
        # Remplacer les quantificateurs
        re_pattern = re_pattern.replace(r'\{', '{').replace(r'\}', '}')
        # Remplacer les classes de caractères POSIX
        re_pattern = re_pattern.replace(r'[[:alpha:]]', r'\w').replace(r'[[:digit:]]', r'\d')
        return re_pattern

class Root:
    def __init__(self):
        self.child = list()
        self.vars = dict()
        self.root = self

    def __len__(self):
        return len(self.child)

    def __contains__(self, value):
        return value in self.child

    def __iter__(self):
        return iter(self.child)

    def add_var(self, name, value):
        self.vars[name] = value

    def get_var(self, name):
        return self.vars.get(name, "")

    def remove_var(self, name):
        return self.vars.pop(name, "")

    def descend_from(self, item):
        return item == self
    
    def find(self, path):
        if '/' in path:
            name, tail = path.split('/', 1)
        else:
            name, tail = path, None
        if name.endswith('*'):
            for item in self:
                if item.name.startswith(name[:-1]):
                    if tail:
                        return item.find(tail)
                    return item
        else:
            for item in self:
                if item.name == name:
                    if tail:
                        return item.find(tail)
                    else:
                        return item
        if path == '.' or not path or path == '/':
            return self
        ans = Error(-1)
        ans.add_description('No such file or directory')
        return ans

    def __repr__(self):
        return 'root'

    @property
    def path(self):
        return '/'
    
    @notImplementedYet
    def login(self, user, password):
        return 'Login successful'


class Directory:
    def __init__(self, parent, name):
        self.child = list()
        self.parent: Directory | Root = parent
        if isinstance(parent, Root):
            self.root: Root = self.parent
        else:
            self.root: Root = self.parent.root
        self.name = name
        self.parent.child.append(self)
    

    def __len__(self):
        return len(self.child)

    def __iter__(self):
        return iter(self.child)


    def __contains__(self, value):
        names = [item.name for item in self.child]
        return value.name in names


    def descend_from(self, item):
        if item == self:
            return True
        if item == self.root:
            return True
        return self.descend_from(item.parent)
        

    @property
    def path(self):
        return self.parent.path + self.name + '/'

    def find(self, path: str):
        if path.startswith('/'):
            return self.root.find(path[1:])
        if '/' in path:
            name, tail = path.split('/', 1)
            if name == '..':
                return self.parent.find(tail)
            elif name == '.':
                return self.find(tail)
            elif name.endswith('*'):
                for item in self:
                    if item.name.startswith(name[:-1]):
                        return item.find(tail)
            target = self.find(name)
            if isinstance(target, Error):
                return target
            return target.find(tail)
        if path == '.':
            return self
        if path == '..':
            return self.parent
        elif path.endswith('*'):
            for item in self:
                if item.name.startswith(path[:-1]):
                    return item
        for item in self:
            if item.name == path:
                return item
        ans = Error(-1)
        ans.add_description('No such file or directory')
        return ans

    def __repr__(self):
        return f'Directory({self.parent}, {self.name})'

    def rename(self, name):
        self.name = name
