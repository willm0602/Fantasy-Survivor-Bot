"""
@survivor the survivor to be updated
@bal the new balance
fs.set_survivor_bal [@survivor] [bal]
"""
from discord.message import Message

from ...command import Admin_Command
from ...db import DB
from ..utils import pairwise, parse_message
from ...exceptions import CommandInputException

async def set_sp_bal(msg: Message):
    db = DB()
    data = parse_message(msg)
    args = data.get("args")

    if len(args) < 2:
        raise CommandInputException("Not enough arguments specified")

    new_players_with_bals = pairwise(args)
    for survivor_with_bal in new_players_with_bals:
        survivor, bal = survivor_with_bal
        if db.get_survivor_by_name_or_false(survivor):
            db.update_survivor_player(survivor, float(bal))
            await msg.channel.send(
                f"Successfully updated balance of {survivor}", reference=msg
            )
        else:
            await msg.channel.send(
                f"Error: {survivor} is not currently a player in the season",
                reference=msg
            )


SET_SURVIVOR_BAL_COMMAND = Admin_Command(
    "set_survivor_bal",
    set_sp_bal,
    "fs.set_survivor_bal [survivor] [bal] updates a users balance",
)
