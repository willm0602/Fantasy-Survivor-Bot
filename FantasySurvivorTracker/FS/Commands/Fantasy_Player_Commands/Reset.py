"""
Let's a user remove all of their bets

fs.reset
"""

from discord.message import Message

from ...Command import Command, User_Command
from ...DB import DB

from ..utils import get_args


async def reset(msg: Message):
    user = msg.author
    db = DB()
    db.remove_all_bets(user)
    await msg.channel.send("succesfully reset all bets")


RESET_COMMAND = User_Command("reset", reset, "fs.reset- removes all bets from a user")
