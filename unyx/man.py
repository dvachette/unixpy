from . import open


def help_ls():
    return """
    ls [path]
    
    List the contents of the current directory or the directory at the specified path.
    """


def help_cd():
    return """
    cd <path>
    
    Change the current directory to the directory at the specified path.
    """


def help_mkdir():
    return """
    mkdir <name>
    
    Create a new directory with the specified name in the current directory.
    """


def help_touch():
    return """
    touch <name>
    
    Create a new file with the specified name in the current directory.
    """


def help_rm():
    return """
    rm <name> [-f]
    
    Remove the file or directory with the specified name. If the directory is not empty, the -f flag can be used to force delete.
    """


def help_exit():
    return """
    exit
    
    Exit the shell.
    """


def help_help():
    return """
    help <command>
    
    Display help information for the specified command.
    """


def help_var():
    return """
    var <option> [name [value]]
    
    Manage shell variables.

    options:
    
    list: List all variables.
    set: Set a variable to the specified value.
    del: Delete a variable.
    get: Get the value of a variable.
    """


def help_open():
    return open.open_.__doc__


def help_():
    return """
    Commands:
    ls
    cd
    mkdir
    touch
    rm
    exit
    help

    Use 'help <command>' for more information on a specific command.
    """
