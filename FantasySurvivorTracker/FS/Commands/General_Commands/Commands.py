

from FS.Commands.General_Commands.Leaderboard import LB_COMMAND
from FS.Commands.General_Commands.List_Survivors import LIST_SURVIVORS_COMMAND
from FS.Commands.General_Commands.checkLocked import CHECK_LOCKED_COMMAND

COMMANDS = [
    LIST_SURVIVORS_COMMAND,
    LB_COMMAND,
    CHECK_LOCKED_COMMAND
]
COMMANDS.sort(
    key = lambda k: k.desc
)