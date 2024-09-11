"""
lets a user view their unspent points

fs.unspent
"""

from discord.message import Message

from ...command import User_Command
from ...db import DB
from ...exceptions import CommandInvalidAccessException


async def view_unspent(msg: Message):
    db = DB()
    user = msg.author
    bal = db.get_unspent_balance(discord_id=user.id)
    if bal is not False:
        bal = round(bal, 4)
        await msg.channel.send(f"You currently have {bal} unspent", reference=msg)
    else:
        raise CommandInvalidAccessException("Error: Unable to get your balance")


VIEW_UNSPENT_COMMAND = User_Command(
    "unspent", view_unspent, "fs.unspent - lets a user view their unspent points"
)
