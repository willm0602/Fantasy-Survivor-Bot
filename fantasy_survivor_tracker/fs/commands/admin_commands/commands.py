from .backup import BACKUP_COMMAND
from .del_fantasy_player import DEL_PLAYER_COMMAND
from .del_survivor_player import DEL_SURVIVOR_COMMAND
from .list_settings import LIST_SETTINGS_COMMAND
from .lock_bets import LOCK_BETS_COMMAND
from .manual_deduct import MANUALLY_DEDUCT_POINTS_COMMAND
from .new_fantasy_player import NEW_FANTASY_PLAYER_COMMAND
from .new_survivor_player import NEW_SURVIVOR_PLAYER_COMMAND
from .read_error_log import READ_ERROR_LOG
from .reset_season import RESET_SEASON_COMMAND
from .restore import RESTORE_COMMAND
from .set_fp_bal import SET_FP_BAL_COMMAND
from .set_not_signed_up_role import SET_NOT_SIGNED_UP_ROLE
from .set_season_role import SET_SEASON_ROLE_COMMAND
from .set_sp_bal import SET_SURVIVOR_BAL_COMMAND
from .unlock_bets import UNLOCK_BETS_COMMAND
from .add_alias import ADD_ALIAS_COMMAND

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
    MANUALLY_DEDUCT_POINTS_COMMAND,
    READ_ERROR_LOG,
    ADD_ALIAS_COMMAND,
]

COMMANDS.sort(key=lambda k: k.desc)
