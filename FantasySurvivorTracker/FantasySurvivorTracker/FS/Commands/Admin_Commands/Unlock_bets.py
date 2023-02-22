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


async def unlock_bets(msg: Message):
    db = DB()
    db.unlock_bets()
    await msg.channel.send("unlocked bets")


UNLOCK_BETS_COMMAND = Admin_Command(
    "unlock",
    unlock_bets,
    "fs.unlock_bets- locks betting for all users",
)
