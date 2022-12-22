
from .Leaderboard import LB_COMMAND
from .List_Survivors import LIST_SURVIVORS_COMMAND
from .checkLocked import CHECK_LOCKED_COMMAND

COMMANDS = [
    LIST_SURVIVORS_COMMAND,
    LB_COMMAND,
    CHECK_LOCKED_COMMAND
]

COMMANDS.sort(
    key = lambda k: k.desc
)