"""
Let's a user make a bet

fs.bet [survivor name] [balance]
"""

from discord.message import Message

from ...Command import Command, User_Command
from ...DB import DB
from ..utils import get_args, pairwise


async def bet(msg: Message):
    user = msg.author
    db = DB()
    args = get_args(msg)
    if len(args) < 2:
        raise Exception("Error: Not Enough Args Specified")

    user_id = db.fp_exists(user)
    player_current_bal = float(db.get_balance(user_id))

    survivors_with_bets = pairwise(args)

    bets = [float(survivor_with_bet[1]) for survivor_with_bet in survivors_with_bets]
    survivors = [survivor_with_bet[0] for survivor_with_bet in survivors_with_bets]

    if sum(bets) > player_current_bal:
        raise Exception(
            f"Error: You are trying to bet a total of {sum(bets)}. You only have {player_current_bal}"
        )

    for survivor in survivors:
        if not db.survivor_exists(survivor):
            raise Exception(f"Error: {survivor} is not a survivor")

    for survivor, amount in survivors_with_bets:
        db.create_bet(user, survivor, float(amount))
    await msg.channel.send("Succesfully Created Bet")


BET_COMMAND = User_Command(
    "bet", bet, "fs.bet [survivor_name] [balance]- creates a bet for that survivor"
)