"""
Let's a user make a bet

fs.bet [survivor name] [balance]
"""

from discord.message import Message

from ...command import BetCommand
from ...db import DB
from ..utils import get_args, pairwise
from ...exceptions import CommandInvalidAccessException
from ...exceptions import ModelInstanceDoesNotExist
from ...exceptions import InvalidBetException


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

    total_amount_betting = 0
    for _, amount in survivors_with_bets:
        total_amount_betting+=float(amount)
    user_unspent = db.get_unspent_balance(discord_id=user.id)
    if round(user_unspent, 3) < round(total_amount_betting, 3):
        raise InvalidBetException(
            f'You don\'t have enough to bet. You have {round(user_unspent, 3)} ' +
            f'but need {total_amount_betting}.'
        )

    for survivor, amount in survivors_with_bets:
        db.create_bet(user, survivor, float(amount))
    await msg.channel.send("successfully Created Bet", reference=msg)


BET_COMMAND = BetCommand(
    "bet", bet, "fs.bet [survivor_name] [balance]- creates a bet for that survivor"
)
