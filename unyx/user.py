from __future__ import annotations

from .FS import FS
from .errors import Error
from werkzeug.security import generate_password_hash, check_password_hash
from ._fs import File
class User:
    def __init__(self, username: str):
        self.username = username
        
    def __repr__(self):
        return f"User {self.username}"
    
    @staticmethod
    def login(username: str, password: str, shell:FS) -> User | Error:
        if isinstance(shell.current.find('/etc/users'), Error):
            return Error(-1)
        users_file:File = shell.current.find('/etc/users')

        for line in users_file.readf():
            if line.startswith(username + ':'):
                _, hashed_password = line.split(':', 1)
                if check_password_hash(hashed_password, password):
                    return User(username)
                else:
                    return Error(-7)
        return Error(-7)
                
