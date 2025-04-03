from .errors import Error


class User:
    names: list[str] = []
    num: int = 0

    def __init__(self):
        self.__class__.num += 1
        self._name: str
        self.uid: int = self.__class__.num

    def getName(self):
        return self._name

    def setName(self, name: str):
        if name not in self.__class__.names:
            self.__class__.names.append(name)
            self._name = name
        else:
            result = Error(-2)
            result.add_description(f'Name {name} already exists')
            return result

    def __repr__(self):
        return f'User {self.id}: {self.name}'
