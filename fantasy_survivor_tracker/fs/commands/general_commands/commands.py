from .check_locked import CHECK_LOCKED_COMMAND
from .leaderboard import LB_COMMAND
from .list_survivors import LIST_SURVIVORS_COMMAND
from .stats import STATS_COMMAND
from .who_bet_on import WHO_BET_COMMAND

COMMANDS = [
    LIST_SURVIVORS_COMMAND,
    LB_COMMAND,
    CHECK_LOCKED_COMMAND,
    STATS_COMMAND,
    WHO_BET_COMMAND,
]


COMMANDS.sort(key=lambda k: k.desc)
