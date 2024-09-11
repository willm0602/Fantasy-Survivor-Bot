"""
Let's a user make a bet

fs.bet [survivor name] [balance]
"""

from discord.message import Message

from ...command import Bet_Command
from ...db import DB
from ..utils import get_args, pairwise
from ...exceptions import CommandInvalidAccessException
from ...exceptions import ModelInstanceDoesNotExist


async def bet(msg: Message):
    user = msg.author
    db = DB()
    args = get_args(msg)
    if len(args) < 2:
        raise CommandInvalidAccessException("Error: Not Enough Args Specified")

    survivors_with_bets = pairwise(args)

    survivors = [survivor_with_bet[0] for survivor_with_bet in survivors_with_bets]

    for survivor in survivors:
        if not db.get_survivor_by_name_or_false(survivor):
            raise ModelInstanceDoesNotExist(f"Error: {survivor} is not a survivor")

    for survivor, amount in survivors_with_bets:
        db.create_bet(user, survivor, float(amount))
    await msg.channel.send("successfully Created Bet", reference=msg)


BET_COMMAND = Bet_Command(
    "bet", bet, "fs.bet [survivor_name] [balance]- creates a bet for that survivor"
)
