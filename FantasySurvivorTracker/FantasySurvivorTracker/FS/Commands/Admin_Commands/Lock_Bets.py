"""
locks the bets

fs.lock
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Admin_Command
from ...DB import DB
from ..utils import parse_message


async def lock_bets(msg: Message):
    db = DB()
    db.lock_bets()
    await msg.channel.send("locked bets")


LOCK_BETS_COMMAND = Admin_Command(
    "lock",
    lock_bets,
    "fs.lock_bets- locks betting for all users",
)
