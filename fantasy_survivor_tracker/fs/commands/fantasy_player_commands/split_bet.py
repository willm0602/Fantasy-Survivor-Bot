"""
Let's a user split their bank between 

fs.split *[survivor name]
"""

from discord.message import Message

from ...command import BetCommand
from ...db import DB
from ..utils import get_args
from ...exceptions import CommandInputException
from ...exceptions import ModelInstanceDoesNotExist
from ...exceptions import UserInputInvalidBetException


async def split(msg: Message):
    user = msg.author
    db = DB()
    args = get_args(msg)
    if len(args) == 0:
        raise CommandInputException("no arguments provided")
    for name in args:
        if not db.get_survivor_by_name_or_false(name):
            raise ModelInstanceDoesNotExist(f"{name} is not a survivor")
    db.remove_all_bets(user)
    bank = db.get_unspent_balance(discord_id=user.id)
    if bank is None:
        raise UserInputInvalidBetException("No money to bet")
    bet_per_player = bank / len(args)
    for name in args[:-1]:
        db.create_bet(user, name, bet_per_player)

    # avoids rounding issues
    bank = db.get_unspent_balance(discord_id=user.id)
    db.create_bet(user, args[-1], bank)
    await msg.channel.send("successfully split", reference=msg)


SPLIT_COMMAND = BetCommand(
    "split",
    split,
    "fs.split [survivor_names]* - splits your remaining bank between each name",
)
