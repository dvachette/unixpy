from .command import Command

from ._ls import Ls as LsCommand
from ._rm import Rm as RmCommand
from ._touch import Touch as TouchCommand
from ._cd import Cd as CdCommand
from ._grep import Grep as GrepCommand
from ._rename import Rename as RenameCommand
from ._cp import Cp as CpCommand
from ._mv import Mv as MvCommand
from ._var import Var as VarCommand
from ._mkdir import Mkdir as MkdirCommand
from ._echo import Echo as EchoCommand
from ._cut import Cut as CutCommand

# List of all commands

# Initialize command instances
touch = TouchCommand()
ls = LsCommand()
rm = RmCommand()
cd = CdCommand()
grep = GrepCommand()
rename = RenameCommand()
cp = CpCommand()
mv = MvCommand()
var = VarCommand()
mkdir = MkdirCommand()
echo = EchoCommand()
cut = CutCommand()