from unyx import starter
from unyx import FS

path = starter.start()
fs = FS.FS(path)
fs.REPL()