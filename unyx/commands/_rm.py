from .command import Command
from .._fs import Directory
from ..errors import Error

class Rm(Command):
    def __init__(self):
        super().__init__("rm")


    def __call__(self, shell, *args):
        """
        Remove files or directories.

        If the first argument is -f or --force, remove non-empty directories.

        Args:
            `shell` : The shell instance.
            `*args`: The arguments passed to the command.

        """
        args = list(args)
        force_remove_directory_flag = False
        if args and args[0].lower() in ['-f', '--force']:
            force_remove_directory_flag = True
            args.pop(0)
        target = shell.current.find(args[0])
        if target == shell.current:
            ans = Error(-5)
            ans.add_description('Cannot delete current directory')
            return ans
        elif isinstance(target, Error):
            return target
        else:
            if isinstance(target, Directory) and len(target):
                if shell.current.descend_from(target):
                    ans = Error(-5)
                    ans.add_description('Cannot delete parent directory')
                    return ans
                else:
                    if force_remove_directory_flag:
                        target.parent.child.remove(target)
                    else:
                        ans = Error(-5)
                        ans.add_description(
                            'Directory not empty, use rm -f <directory> to force delete'
                        )
                        return ans
            else:
                target.parent.child.remove(target)