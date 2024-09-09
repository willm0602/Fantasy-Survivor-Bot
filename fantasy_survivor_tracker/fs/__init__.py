from .commands.commands import COMMANDS as NON_HELP_COMMANDS
from .commands.help_command import HELP_COMMAND

COMMANDS = [*NON_HELP_COMMANDS, HELP_COMMAND]

__all__ = [COMMANDS]
