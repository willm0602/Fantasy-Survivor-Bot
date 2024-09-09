from .all_in import ALL_IN_COMMAND
from .bet import BET_COMMAND
from .list_bets import LIST_BETS_COMMAND
from .quit import QUIT_COMMAND
from .remove_bet import REMOVE_BET_COMMAND
from .reset import RESET_COMMAND
from .signup import SIGNUP_COMMAND
from .split_bet import SPLIT_COMMAND
from .unspent import VIEW_UNSPENT_COMMAND
from .view import VIEW_BALANCE_COMMAND

COMMANDS = [
    SIGNUP_COMMAND,
    VIEW_BALANCE_COMMAND,
    BET_COMMAND,
    QUIT_COMMAND,
    LIST_BETS_COMMAND,
    REMOVE_BET_COMMAND,
    RESET_COMMAND,
    SPLIT_COMMAND,
    ALL_IN_COMMAND,
    VIEW_UNSPENT_COMMAND,
]
COMMANDS.sort(key=lambda k: k.desc)
