from typing import List

from ..command import Command
from .admin_commands.commands import COMMANDS as Admin_Commands
from .fantasy_player_commands.commands import COMMANDS as FP_COMMANDS
from .general_commands.commands import COMMANDS as GEN_COMMANDS

COMMANDS: List[Command] = [*Admin_Commands, *FP_COMMANDS, *GEN_COMMANDS]
COMMANDS.sort(key=lambda k: k.desc)
