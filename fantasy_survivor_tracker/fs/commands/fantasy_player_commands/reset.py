"""
Let's a user remove all of their bets

fs.reset
"""

from discord.message import Message

from ...command import Command
from ...db import DB


async def reset(msg: Message):
    user = msg.author
    db = DB()
    db.remove_all_bets(user)
    await msg.channel.send("successfully reset all bets", reference=msg)


RESET_COMMAND = Command("reset", reset, "fs.reset- removes all bets from a user")
