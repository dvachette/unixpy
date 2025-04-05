from .ls import Ls as LsCommand
from .command import Command
from .rm import Rm as RmCommand
from .touch import Touch as TouchCommand

# Initialize command instances
touch = TouchCommand()
ls = LsCommand()
rm = RmCommand()