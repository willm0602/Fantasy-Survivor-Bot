"""
Let's a user remove a bet

fs.remove_bet [bet id]
"""

from discord.message import Message

from ...command import BetCommand
from ...db import DB
from ..utils import get_args
from ...exceptions import CommandInputException


async def remove_bet(msg: Message):
    user = msg.author
    db = DB()
    args = get_args(msg)
    if len(args) == 0:
        raise CommandInputException("Missing argument: needs bet id passed in")
    survivor_name = args[0]
    db.remove_bet(survivor_name, user)
    await msg.channel.send("successfully removed bet", reference=msg)


REMOVE_BET_COMMAND = BetCommand(
    "remove_bet",
    remove_bet,
    "fs.remove_bet [survivor name]- removes all bets you made for the given survivor",
)
