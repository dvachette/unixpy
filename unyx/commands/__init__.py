from .command import Command

from .ls import Ls as LsCommand
from .rm import Rm as RmCommand
from .touch import Touch as TouchCommand
from .cd import Cd as CdCommand
from .grep import Grep as GrepCommand

# List of all commands

# Initialize command instances
touch = TouchCommand()
ls = LsCommand()
rm = RmCommand()
cd = CdCommand()
grep = GrepCommand()