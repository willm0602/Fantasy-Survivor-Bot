"""
fs.reset_season
"""


from discord.message import Message

from ...command import Admin_Command
from ...db import DB


async def reset_season(msg: Message):
    db = DB()
    db.reset_season()
    await msg.channel.send("successfully reset season", reference=msg)


RESET_SEASON_COMMAND = Admin_Command(
    "season_reset",
    reset_season,
    "fs.season_reset resets the whole season (ONLY RUN WHEN SEASON IS DONE, DELETES ALL PROGRESS WITH NO BACKUP)",
)
