import unittest


class File:
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
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

    @property
    def path(self):
        return self.parent.path + self.name

    def read(self, start=0, end=None):
        if end is None:
            return self.data[start:]
        return self.data[start:end]

    def write(self, content):
        self.data = ' '.join(content).split('\\n')

    def move(self, target):
        self.parent.child.remove(self)
        self.parent = target
        self.parent.child.append(self)

    def append(self, content):
        self.data.extend(' '.join(content).split('\\n'))

    def insert(self, line, content):
        self.data.insert(line, content)

    def delete(self, line):
        del self.data[line]

    def edit(self, line, content):
        self.data[line] = content

    def find(self, path):
        return 'No such file or directory'

    def rename(self, name):
        self.name = name


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
        return self.vars.get(name, None)

    def remove_var(self, name):
        return self.vars.pop(name, None)

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
        return 'No such file or directory'

    def __repr__(self):
        return 'root'

    @property
    def path(self):
        return '/'

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
            if target == 'No such file or directory':
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
        return 'No such file or directory'

    def __repr__(self):
        return f'Directory({self.parent}, {self.name})'

    def rename(self, name):
        self.name = name


class TestFileSystem(unittest.TestCase):
    def setUp(self):
        self.root = Root()
        self.dir1 = Directory(self.root, 'dir1')
        self.dir2 = Directory(self.dir1, 'dir2')
        self.file1 = File(self.dir1, 'file1')
        self.file2 = File(self.dir2, 'file2')
        self.file1.data = 'Hello'
        self.file2.data = 'World'

    def test_initialization(self):
        self.assertEqual(self.root.child, [self.dir1])
        self.assertEqual(self.dir1.child, [self.dir2, self.file1])
        self.assertEqual(self.dir2.child, [self.file2])
        self.assertEqual(self.file1.name, 'file1')
        self.assertEqual(self.file2.name, 'file2')

    def test_repr_str(self):
        self.assertEqual(repr(self.file1), 'File(Directory(root, dir1),file1)')
        self.assertEqual(str(self.file1), 'file1')
        self.assertEqual(repr(self.dir1), 'Directory(root, dir1)')

    def test_path_property(self):
        self.assertEqual(self.file1.path, '/dir1/file1')
        self.assertEqual(self.dir2.path, '/dir1/dir2/')

    def test_find_method(self):
        self.assertEqual(self.root.find('dir1/dir2/file2'), self.file2)
        self.assertEqual(self.dir1.find('dir2/file2'), self.file2)
        self.assertEqual(self.dir1.find('..'), self.root)
        self.assertEqual(self.dir2.find('.'), self.dir2)
        self.assertEqual(self.root.find('dir1/.'), self.dir1)
        self.assertEqual(self.dir1.find('file*'), self.file1)
        self.assertEqual(
            self.root.find('dir1/dir2/file3'), 'No such file or directory'
        )


if __name__ == '__main__':
    unittest.main()
