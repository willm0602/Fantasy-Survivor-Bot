'''
Let's a user make a bet

fs.bet [survivor name] [balance]
'''

from discord.message import Message

from FS.Command import Command, User_Command
from FS.DB import DB

from ..utils import get_args


async def bet(msg: Message):
    user = msg.author
    db = DB()
    args = get_args(msg)
    user_id = db.fp_exists(user)
    player_current_bal = db.get_balance(user_id)
    survivor_name = args[0]
    amount = float(args[1])
    if amount > player_current_bal or amount <= 0:
        await msg.channel.send('Error: Invalid Bet Amount')
        return
    db.create_bet(
        user,
        survivor_name,
        amount
    )
    await msg.channel.send('Succesfully Created Bet')


BET_COMMAND = User_Command(
    'bet',
    bet,
    'fs.bet [survivor_name] [balance]- creates a bet for that survivor'
)
