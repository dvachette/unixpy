from ..errors import Error
from ..unyxutils import notImplementedYet
from .__bases import _FSObject
from .__bases import _ContainerFSObject
from typing import Iterable


class Root(_ContainerFSObject):
    """ Root class for the file system.
    It contains the root directory and provides methods to manage
    the file system.
    It is a singleton class, meaning there is only one instance of it.
    It is used to manage the file system and provide access to the
    directories and files in the file system.

    ## Attributes:
        child (list): List of child directories and files.
        vars (dict): Dictionary of variables.
        root (Root): Reference to the root directory.
    ## Methodes:
        __len__() ->(int):
            Returns the number of child directories and files.
        __contains__(value) -> (bool) :
            Returns True if the value is in the child list.
        __iter__() -> (Iterable):
            Returns an iterator for the child list.
        add_var(name, value) -> (None):
            Adds a variable to the vars dictionary.
        get_var(name) -> (str):
            Gets a variable from the vars dictionary.
        remove_var(name) -> (str):
            Removes a variable from the vars dictionary.
        descend_from(item) -> (bool):
            Returns True if the item is a descendant of this directory.
        find(path) -> (FSBaseObject):
            Finds a directory or file by its path.
        __repr__() -> (str):
            Returns a string representation of the root directory.
        login(user, password) -x (Exception) :
            Logs in to the file system. [NIY]
        path -> (str):
            Returns the path of the root directory.
    ## Properties:
        path (str): Path of the root directory.

    ## Examples:
    >>> root = Root()

    ### Variables system
    >>> root.add_var('key', 'value')

    >>> root.get_var('key')
    'value'
    >>> root.remove_var('key')
    'value'
    >>> root.get_var('key')
    ''
    """

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
        return self.vars.get(name, '')

    def remove_var(self, name):
        return self.vars.pop(name, '')

    def descend_from(self, item):
        return item == self

    def find(self, path):
        if path.startswith('/'):
            path = path[1:]
        if '/' in path:
            name, tail = path.split('/', 1)
        else:
            name, tail = path, None
        if name.endswith('*'):
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
                if tail:
                    return matches[0].find(tail)
                return matches[0]
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
