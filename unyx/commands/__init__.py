from typing import Callable

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
from ._open import Open as OpenCommand
# List of all commands

# Initialize command instances
touch:Callable = TouchCommand()
ls:Callable = LsCommand()
rm:Callable = RmCommand()
cd:Callable = CdCommand()
grep:Callable = GrepCommand()
rename:Callable = RenameCommand()
cp:Callable = CpCommand()
mv:Callable = MvCommand()
var:Callable = VarCommand()
mkdir:Callable = MkdirCommand()
echo:Callable = EchoCommand()
cut:Callable = CutCommand()
open_:Callable = OpenCommand()

