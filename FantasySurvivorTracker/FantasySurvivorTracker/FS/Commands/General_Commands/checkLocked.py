"""
checks if voting is locked
fs.check_locked
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Command
from ...DB import DB


async def is_locked(msg: Message):
    db = DB()
    channel: TextChannel = msg.channel
    if db.get_setting("bettingLocked") == "no":
        await channel.send(f"Betting is not locked")
    else:
        await channel.send(f"Betting is locked")


CHECK_LOCKED_COMMAND = Command(
    "check_locked",
    is_locked,
    "fs.check_locked checks if betting is locked",
)
