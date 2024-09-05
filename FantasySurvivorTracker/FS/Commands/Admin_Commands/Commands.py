from FantasySurvivorTracker.FS.Commands.Admin_Commands.ManualDeduct import MANUALLY_DEDUCT_POINTS_COMMAND
from .Backup import BACKUP_COMMAND
from .Del_Fantasy_Player import DEL_PLAYER_COMMAND
from .Del_Survivor_Player import DEL_SURVIVOR_COMMAND
from .Lock_Bets import LOCK_BETS_COMMAND
from .New_Fantasy_Player import NEW_FANTASY_PLAYER_COMMAND
from .New_Survivor_Player import NEW_SURVIVOR_PLAYER_COMMAND
from .Reset_Season import RESET_SEASON_COMMAND
from .Restore import RESTORE_COMMAND
from .Set_FP_Bal import SET_FP_BAL_COMMAND
from .Set_Season_Role import SET_SEASON_ROLE_COMMAND
from .Set_SP_Bal import SET_SURVIVOR_BAL_COMMAND
from .Unlock_bets import UNLOCK_BETS_COMMAND
from .Set_Not_Signed_Up_Role import SET_NOT_SIGNED_UP_ROLE
from .List_Settings import LIST_SETTINGS_COMMAND

COMMANDS = [
    NEW_FANTASY_PLAYER_COMMAND,
    DEL_PLAYER_COMMAND,
    SET_FP_BAL_COMMAND,
    NEW_SURVIVOR_PLAYER_COMMAND,
    SET_SURVIVOR_BAL_COMMAND,
    DEL_SURVIVOR_COMMAND,
    BACKUP_COMMAND,
    RESTORE_COMMAND,
    LOCK_BETS_COMMAND,
    UNLOCK_BETS_COMMAND,
    RESET_SEASON_COMMAND,
    SET_SEASON_ROLE_COMMAND,
    SET_NOT_SIGNED_UP_ROLE,
    LIST_SETTINGS_COMMAND,
    MANUALLY_DEDUCT_POINTS_COMMAND
]

COMMANDS.sort(key=lambda k: k.desc)
