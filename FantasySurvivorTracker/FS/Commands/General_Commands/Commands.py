from .checkLocked import CHECK_LOCKED_COMMAND
from .Leaderboard import LB_COMMAND
from .List_Survivors import LIST_SURVIVORS_COMMAND
from .Stats import STATS_COMMAND

COMMANDS = [LIST_SURVIVORS_COMMAND, LB_COMMAND, CHECK_LOCKED_COMMAND, STATS_COMMAND]

COMMANDS.sort(key=lambda k: k.desc)
