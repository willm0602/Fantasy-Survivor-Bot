import aiocron
import pytz
from .FS.DB import DB

PST = pytz.timezone("US/Pacific")


# locks betting automatically at 5:00 PST/8:00 EST so users can't bet after
# Survivor airs till scores are updated
@aiocron.crontab("0 17 * * 3", tz=PST)
def autolock_bot():
    DB().set_setting("bettingLocked", "yes")
