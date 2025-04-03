import re
from .__bases import __FSObject
from .__bases import __ContainerFSObject
from ..errors import Error
from .root import Root

class File(__FSObject):
    def __init__(self, parent, name):
        self.name = name
        self.parent: __ContainerFSObject = parent
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
            for i, data in enumerate(content):
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
                    l_fields.append(int(field) - 1)
                else:
                    ans = Error(-2)
                    ans.add_description('Invalid field')
                    return ans
            else:
                start, end = field.split('-')
                if start.isdigit() and end.isdigit():
                    l_fields.extend(range(int(start) - 1, int(end)))
                else:
                    ans = Error(-2)
                    ans.add_description('Invalid field')
                    return ans
        ans = list()
        for line in self.data:
            linesplit = line.split(separator)
            ans.append(separator.join([linesplit[i] for i in l_fields]))
        return '\n'.join(ans)

    def grep(self, pattern):
        ans = list()
        pattern = self.__class__.convert_grep_to_re(pattern)
        for line in self.data:
            if re.search(pattern, line):
                ans.append(line)
        return '\n'.join(ans)

    @staticmethod
    def convert_grep_to_re(grep_pattern: str) -> str:
        # Remplacer les groupes de capture
        re_pattern = grep_pattern.replace(r'\(', '(').replace(r'\)', ')')
        # Remplacer les alternatives
        re_pattern = re_pattern.replace(r'\|', '|')
        # Remplacer les quantificateurs
        re_pattern = re_pattern.replace(r'\{', '{').replace(r'\}', '}')
        # Remplacer les classes de caractères POSIX
        re_pattern = re_pattern.replace(r'[[:alpha:]]', r'\w').replace(
            r'[[:digit:]]', r'\d'
        )
        return re_pattern

