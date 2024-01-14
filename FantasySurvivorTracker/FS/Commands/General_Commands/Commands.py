from .checkLocked import CHECK_LOCKED_COMMAND
from .Leaderboard import LB_COMMAND
from .List_Survivors import LIST_SURVIVORS_COMMAND
from .Stats import STATS_COMMAND
from .Who_Bet import WHO_BET_COMMAND

COMMANDS = [
    LIST_SURVIVORS_COMMAND,
    LB_COMMAND,
    CHECK_LOCKED_COMMAND,
    STATS_COMMAND,
    WHO_BET_COMMAND,
]


COMMANDS.sort(key=lambda k: k.desc)
