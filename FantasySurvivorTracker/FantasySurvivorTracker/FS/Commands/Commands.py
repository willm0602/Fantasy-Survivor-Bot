from typing import List

from ..Command import Command
from .Admin_Commands.Commands import COMMANDS as Admin_Commands
from .Fantasy_Player_Commands.FP_Commands import COMMANDS as FP_COMMANDS
from .General_Commands.Commands import COMMANDS as GEN_COMMANDS

COMMANDS: List[Command] = [*Admin_Commands, *FP_COMMANDS, *GEN_COMMANDS]
COMMANDS.sort(key=lambda k: k.desc)
