from __future__ import annotations

class File:
    def __init__(self, name:str, parent:'Directory', content:str=""):
        self.name = name
        self.parent = parent
        self.content = content

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def path(self):
        return self.parent.path() + '/' + self.name

    def read(self):
        return self.content
    
    def write(self, content:str):
        self.content = content

    def append(self, content:str):
        self.content += content
    
    def delete(self):
        self.parent.remove(self)

class Directory:
    def __init__(self, name:str, parent:'Directory'|None=None):
        self.name = name
        self.parent = parent
        self.children = set()

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def path(self):
        if self.parent:
            return self.parent.path() + '/' + self.name
        return self.name
    
    def add(self, child:'File'|'Directory'):
        self.children.add(child)

    def remove(self, child:'File'|'Directory'):
        if child in self.children:
            self.children.remove(child)
        
    def find(self, name:str):
        for child in self.children:
            if child.name == name:
                return child
        return None
    
