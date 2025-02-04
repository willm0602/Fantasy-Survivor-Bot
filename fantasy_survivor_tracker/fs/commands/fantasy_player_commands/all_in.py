"""
Let's a user bet all of their remaining bank on one player

fs.all_in [survivor name]
"""

from discord.message import Message

from ...command import BetCommand
from ...db import DB
from ..utils import get_args
from ...exceptions import CommandInputException
from ...exceptions import ModelInstanceDoesNotExist


async def all_in(msg: Message):
    user = msg.author
    db = DB()
    user_id = db.get_registed_user_or_false(user)
    args = get_args(msg)
    if len(args) == 0:
        raise CommandInputException("no arguments provided")
    survivor = db.get_survivor_by_name_or_false(args[0])
    if survivor is False:
        raise ModelInstanceDoesNotExist(f"{args[0]} is not a survivor")

    bank = db.get_unspent_balance(user_id)
    if bank <= 0:
        raise CommandInputException("Error: You have no money to bet")

    db.create_bet(user, args[0], bank)
    await msg.channel.send(f"successfully went all in on {args[0]}", reference=msg)


ALL_IN_COMMAND = BetCommand(
    "all_in", all_in, "fs.all_in [survivor_names] - Lets a user go all in with a bet"
)
