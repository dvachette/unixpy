# Unixpy
A unix like simulator (actually a learning project)
## what can unyx do ?
Unyx is a python program that can simulate a unix console behaviour
It is fully written in python
You can create files systems, move into it, edit, create, read and delete files and directory
You can also create multiple instances, by using the starter

## What are the requirements for Unyx ?
you only need python 3.10 +, all the dependencies are available in the standard lib

## How do you use unyx ?
First you need to import the module's dependencies

```
from unyx import starter 
from unyx import shell
```
Import the starter program (equivalent to the boot menu, it helps you to select on which instance ou want to work)

Import the shell program, which will handle the instance and all the file system


```
path = starter.start()
shell.Shell(path).run()
```

`starter.start()` makes you select an instance and returns its path

`shell.Shell(path).run()` This is the main program, which will launch the shell 

