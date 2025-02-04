"""
locks the bets

fs.lock
"""


from discord.message import Message

from ...command import AdminCommand
from ...db import DB


async def unlock_bets(msg: Message):
    db = DB()
    db.unlock_bets()
    await msg.channel.send("unlocked bets", reference=msg)


UNLOCK_BETS_COMMAND = AdminCommand(
    "unlock",
    unlock_bets,
    "fs.unlock_bets- locks betting for all users",
)
