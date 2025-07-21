from unyx import FS
fs = FS.FS("instances/marche.unyx")
fs.removefile("test.txt")
fs.makefile("test.txt")
fs.writeinfile("test.txt", b"test")

print(fs.open("test.txt", "r"))