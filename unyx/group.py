from __future__ import annotations

from .errors import Error
from .user import User


class Group:
    _instances: list[Group] = list()

    def __init__(self):
        self._name: str
        self._gid: int = len(self.__class__._instances)
        self._users: set[User] = set()
        self.__class__._instances.append(self)
        self._name: str

    def setName(self, name: str) -> Error | None:
        if name not in [group._name for group in self.__class__._instances]:
            self._name = name
        else:
            ans: Error = Error(-2)
            ans.add_description(f"name '{name}' is already taken")
            return ans

    def addUser(self, user: User) -> Error | None:
        previousLenght: int = len(self._users)
        self._users.add(user)
        # TODO add the group to the user

        if len(self._users) == previousLenght:
            ans = Error(-2)
            ans.add_description(
                f"user '{user.getName()} is already in this group"
            )
            return ans

    @classmethod
    def getGroupByName(cls, name: str) -> Group | Error:
        ans = Error(-2)
        ans.add_description(f"There is no group named '{name}'")
        for group in cls._instances:
            if group._name == name:
                ans = group
        return ans

    @classmethod
    def getGroupByGid(cls, gid: int) -> Group | Error:
        ans = Error(-2)
        ans.add_description(f"There is no group with the id  '{gid}'")
        for group in cls._instances:
            if group._gid == gid:
                ans = group
        return ans

    def __contains__(self, user: User) -> bool:
        return user in self._users
    