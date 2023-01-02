from .FS.DB import DB
import aiocron


@aiocron.crontab("17 18 * * 0")
def autolock_bot():
    DB().set_setting("bettingLocked", "yes")
