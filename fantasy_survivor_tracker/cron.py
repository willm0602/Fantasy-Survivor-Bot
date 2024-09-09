import aiocron
import pytz

from .fs.db import DB

PST = pytz.timezone("US/Pacific")


# locks betting automatically at 5:00 PST/8:00 EST so users can't bet after
# Survivor airs till scores are updated
@aiocron.crontab("0 17 * * 3", tz=PST)
def autolock_bot():
    DB().set_setting("bettingLocked", "yes")
    should_deduct_points = DB().get_setting("deductPointsWeekly") == "yes"
    if should_deduct_points:
        DB().deduct_unspent_points_by_five_percent()
