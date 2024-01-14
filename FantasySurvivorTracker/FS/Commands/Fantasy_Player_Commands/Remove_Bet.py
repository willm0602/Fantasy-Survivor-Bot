"""
Let's a user remove a bet

fs.remove_bet [bet id]
"""

from discord.message import Message

from ...Command import Command, Bet_Command
from ...DB import DB
from ..utils import get_args


async def remove_bet(msg: Message):
    user = msg.author
    db = DB()
    args = get_args(msg)
    if len(args) == 0:
        raise Exception("Missing argument: needs bet id passed in")
    survivor_name = args[0]
    db.remove_bet(survivor_name, user)
    await msg.channel.send("succesfully removed bet")


REMOVE_BET_COMMAND = Bet_Command(
    "remove_bet",
    remove_bet,
    "fs.remove_bet [survivor name]- removes all bets you made for the given survivor",
)
