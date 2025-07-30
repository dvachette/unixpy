
from ..errors import Error
from .__bases import _ContainerFSObject
from .__bases import _FSObject
from .root import Root
class Directory(_ContainerFSObject):
    def __init__(self, parent, name):
        self.child = list()
        self.parent: _ContainerFSObject = parent
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
        return item.path in self.path

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
                # Handling multiple to prevent arbitrary matches
                # for example, /test* will match /test1, /test2, etc.
                # so we need to raise an error if there are multiple matches
                # and return the matched item if there is only one match
                # Handling single match
                matches = [item for item in self if item.name.startswith(name[:-1])]
                if len(matches) > 1:
                    ans = Error(-1)
                    ans.add_description('Ambiguous match')
                    ans.add_description(f'Matches: {", ".join([item.name for item in matches])}')
                    return ans
                elif len(matches) == 1:
                    return matches[0].find(tail)
            target = self.find(name)
            if isinstance(target, Error):
                return target
            return target.find(tail)
        if path == '.':
            return self
        if path == '..':
            return self.parent
        elif path.endswith('*'):
            # Handling multiple to prevent arbitrary matches
            # for example, /test* will match /test1, /test2, etc.
            # so we need to raise an error if there are multiple matches
            # and return the matched item if there is only one match
            matches = [item for item in self if item.name.startswith(path[:-1])]
            if len(matches) > 1:
                ans = Error(-1)
                ans.add_description('Ambiguous match')
                ans.add_description(f'Matches: {", ".join([item.name for item in matches])}')
                return ans
            elif len(matches) == 1:
                return matches[0]
        # Handling single match
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
