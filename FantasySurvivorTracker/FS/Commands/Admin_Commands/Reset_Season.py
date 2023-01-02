"""
fs.reset_season
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Admin_Command
from ...DB import DB


async def reset_season(msg: Message):
    db = DB()
    db.reset_season()
    await msg.channel.send("Succesfully reset season")


RESET_SEASON_COMMAND = Admin_Command(
    "season_reset",
    reset_season,
    "fs.season_reset resets the whole season (ONLY RUN WHEN SEASON IS DONE, DELETES ALL PROGRESS WITH NO BACKUP)",
)
