from .All_In import ALL_IN_COMMAND
from .Bet import BET_COMMAND
from .List_Bets import LIST_BETS_COMMAND
from .Quit import QUIT_COMMAND
from .Remove_Bet import REMOVE_BET_COMMAND
from .Reset import RESET_COMMAND
from .Signup import SIGNUP_COMMAND
from .Split_Bet import SPLIT_COMMAND
from .View import VIEW_BALANCE_COMMAND
from .Unspent import VIEW_UNSPENT_COMMAND

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
