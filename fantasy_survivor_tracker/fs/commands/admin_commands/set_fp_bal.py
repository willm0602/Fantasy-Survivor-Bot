"""
@user the user to be updated
@bal the new balance
fs.set_fp_bal [@user] [bal]
"""


from discord.member import Member
from discord.message import Message

from ...command import AdminCommand
from ...db import DB
from ..utils import parse_message
from ...exceptions import CommandInputException
from ...exceptions import ModelInstanceDoesNotExist


async def set_fp_bal(msg: Message):
    db = DB()
    data = parse_message(msg)
    args = data.get("args")
    if len(args) != 2:
        raise CommandInputException("Not enough arguments specified")
    balance = float(args[1])
    user: Member
    user = msg.mentions[0]
    if db.get_registed_user_or_false(user):
        db.update_balance(user, balance)
        await msg.channel.send(
            "Successfully updated balance of " + user.display_name, reference=msg
        )
    else:
        raise ModelInstanceDoesNotExist("User doesn't exist")


SET_FP_BAL_COMMAND = AdminCommand(
    "set_fp_bal",
    set_fp_bal,
    "fs.set_fp_bal [@user] [bal] updates a users balance",
)
