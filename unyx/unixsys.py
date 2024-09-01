class File:
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.data = None
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
        return self.parent.path  + self.name
    

class Root:
    def __init__(self):
        self.child = list()

    def __len__(self):
        return len(self.child)

    def __contains__(self, value):
        return value in self.child
    
    def __iter__(self):
        return iter(self.child)
    
    def find(self, path):
        if "/" in path:
            name, tail = path.split("/",1)
        else:
            name, tail = path, None
        if name.endswith("*"):
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
        return "No such file or directory"
    def __repr__(self):
        return 'root'
    @property
    def path(self):
        return "/"
    
class Directory:
    def __init__(self, parent, name):
        self.child = list()
        self.parent:Directory|Root = parent
        if isinstance(parent, Root):
            self.root:Root = self.parent
        else:
            self.root:Root = self.parent.root
        self.name = name
        self.parent.child.append(self)
    def __len__(self):
        return len(self.child)
    
    def __iter__(self):
        return iter(self.child)
    
    @property
    def path(self):
        return self.parent.path+self.name+"/"
    
    def find(self, path:str):

        if path.startswith("/"):
            return self.root.find(path[1:])
        if "/" in path:
            name, tail = path.split("/",1)
            if name == "..":
                return self.parent.find(tail)
            elif name == ".":
                return self.find(tail)
            elif name.endswith("*"):
                for item in self:
                    if item.name.startswith(name[:-1]):
                        return item.find(tail)
            return self.find(name).find(tail)
        if path == ".":
            return self
        if path == "..":
            return self.parent
        elif name.endswith("*"):
                for item in self:
                    if item.name.startswith(name[:-1]):
                        return item.find(tail)
        for item in self:
            if item.name == path:
                return item
    
    def __repr__(self):
        return f'Directory({self.parent}, {self.name})'


