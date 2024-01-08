"""
lets a user view their bank

fs.view_bal
"""

from discord.message import Message

from ...Command import User_Command
from ...DB import DB


async def view_balance(msg: Message):
    db = DB()
    user = msg.author
    user_id = db.get_registed_user_or_false(user)
    bal = db.get_unspent_balance(user_id)
    if bal is not False:
        bal = db.get_total_bal(user_id)
        bal = round(bal, 4)
        await msg.channel.send(f"You currently have a balance of {bal}")
    else:
        raise Exception("Error: Unable to get your balance")


VIEW_BALANCE_COMMAND = User_Command(
    "view_bal", view_balance, "fs.view_bal - lets a user view their balance"
)
