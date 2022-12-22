from FS.Commands.Admin_Commands.Mod_SP_Bal import MOD_SURVIVOR_BAL_COMMAND

from .Del_Fantasy_Player import DEL_PLAYER_COMMAND
from .New_Fantasy_Player import NEW_FANTASY_PLAYER_COMMAND
from .New_Survivor_Player import NEW_SURVIVOR_PLAYER_COMMAND
from .Set_FP_Bal import SET_FP_BAL_COMMAND
from .Del_Survivor_Player import DEL_SURVIVOR_COMMAND
from .Backup import BACKUP_COMMAND
from .Restore import RESTORE_COMMAND
from .Lock_Bets import LOCK_BETS_COMMAND
from .Unlock_bets import UNLOCK_BETS_COMMAND

COMMANDS = [
    NEW_FANTASY_PLAYER_COMMAND,
    DEL_PLAYER_COMMAND,
    SET_FP_BAL_COMMAND,
    NEW_SURVIVOR_PLAYER_COMMAND,
    MOD_SURVIVOR_BAL_COMMAND,
    DEL_SURVIVOR_COMMAND,
    BACKUP_COMMAND,
    RESTORE_COMMAND,
    LOCK_BETS_COMMAND,
    UNLOCK_BETS_COMMAND
]
COMMANDS.sort(
    key = lambda k: k.desc
)
