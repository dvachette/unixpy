from __future__ import annotations

from .errors import Error
from werkzeug.security import generate_password_hash, check_password_hash
from ._fs import File
class User:
    def __init__(self, username: str, user_id: int):
        self.username:str = username
        self.user_id:int = user_id
        
    def __repr__(self):
        return f"User {self.username}"
    
    @staticmethod
    def login(username: str, password: str, shell) -> User | Error:
        if isinstance(shell.current.find('/etc/users'), Error):
            return Error(-1)
        users_file:File = shell.current.find('/etc/users')

        for line in users_file.readf():
            if line.startswith(username + ':'):
                username, user_id, hashed_password = line.split(':', 2)
                if check_password_hash(hashed_password, password):
                    return User(username, int(user_id))
                else:
                    return Error(-7)
        return Error(-7)
                
