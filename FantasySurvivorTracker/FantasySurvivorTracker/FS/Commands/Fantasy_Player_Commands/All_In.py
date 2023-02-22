"""
Let's a user bet all of their remaining bank on one player

fs.all_in [survivor name]
"""

from discord.message import Message

from ...Command import Command, User_Command
from ...DB import DB
from ..utils import get_args


async def all_in(msg: Message):
    user = msg.author
    db = DB()
    user_id = db.fp_exists(user)
    args = get_args(msg)
    if len(args) == 0:
        raise Exception("no arguments provided")
    survivor = db.survivor_exists(args[0])
    if survivor is False:
        raise Exception(f"{args[0]} is not a survivor")

    bank = db.get_balance(user_id)
    if bank <= 0:
        raise Exception("Error: You have no money to bet")

    for name in args:
        db.create_bet(user, name, bank)
    await msg.channel.send(f"successfully went all in on {args[0]}")


ALL_IN_COMMAND = User_Command(
    "all_in", all_in, "fs.all_in [survivor_names] - Lets a user go all in with a bet"
)