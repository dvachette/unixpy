from .errors import Error
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    instances = list()
    num: int = 0

    def __init__(self):
        self.__class__.num += 1
        self._name: str
        self.uid: int = self.__class__.num

    def getName(self):
        return self._name

    def setName(self, name: str):
        if any(name == user.name for user in self.__class__.instances):
            self.__class__.instances.append(self)
            self._name = name
        else:
            result = Error(-2)
            result.add_description(f'User :{name} already exists')
            return result

    def __repr__(self):
        return f'User {self.id}: {self.name}'

    @classmethod
    def getUserByUid(cls, uid: int):
        for instance in cls.instances:
            if instance.uid == uid:
                return instance
        ans = Error(-7)
        ans.add_description(f'User with uid {uid} not found')
        return ans