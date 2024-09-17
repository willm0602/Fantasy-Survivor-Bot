"""
locks the bets

fs.lock
"""


from discord.message import Message

from ...command import AdminCommand
from ...db import DB


async def lock_bets(msg: Message):
    db = DB()
    db.lock_bets()
    await msg.channel.send("locked bets", reference=msg)


LOCK_BETS_COMMAND = AdminCommand(
    "lock",
    lock_bets,
    "fs.lock_bets- locks betting for all users",
)
