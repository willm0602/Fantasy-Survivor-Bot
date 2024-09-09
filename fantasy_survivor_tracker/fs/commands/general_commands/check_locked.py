"""
checks if voting is locked
fs.check_locked
"""


from discord.channel import TextChannel
from discord.message import Message

from ...command import Command
from ...db import DB


async def is_locked(msg: Message):
    db = DB()
    channel: TextChannel = msg.channel
    if db.get_setting("bettingLocked") == "no":
        await channel.send("Betting is not locked", reference=msg)
    else:
        await channel.send("Betting is locked", reference=msg)


CHECK_LOCKED_COMMAND = Command(
    "check_locked",
    is_locked,
    "fs.check_locked checks if betting is locked",
)
