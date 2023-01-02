"""
Let's a user remove a bet

fs.remove_bet [bet id]
"""

from discord.message import Message

from ...Command import Command, User_Command
from ...DB import DB

from ..utils import get_args


async def remove_bet(msg: Message):
    user = msg.author
    db = DB()
    args = get_args(msg)
    if len(args) == 0:
        raise Exception("Missing argument: needs bet id passed in")
    try:
        survivor_name = args[0]
    except ValueError:
        raise Exception("Error: Bet ID must be an integer")
    db.remove_bet(survivor_name, user)
    await msg.channel.send("succesfully removed bet")


REMOVE_BET_COMMAND = User_Command(
    "remove_bet", remove_bet, "fs.remove_bet [id]- removes the bet with the given id"
)
