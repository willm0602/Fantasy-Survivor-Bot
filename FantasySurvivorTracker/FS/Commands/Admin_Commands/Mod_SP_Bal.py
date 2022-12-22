"""
@survivor the survivor to be updated
@bal the new balance
fs.set_survivor_bal [@survivor] [bal]
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Admin_Command
from ...DB import DB
from ..utils import parse_message


async def mod_sp_bal(msg: Message):
    db = DB()
    data = parse_message(msg)
    args = data.get("args")
    if len(args) != 2:
        raise Exception("Not enough arguments specified")
    balance = float(args[1])
    player = args[0]
    if db.survivor_exists(player):
        db.update_survivor_player(player, balance)
        await msg.channel.send(f"Successfully updated balance of {player}")
    else:
        raise Exception(f"Error: {player} is not currently a player in the season")
    
MOD_SURVIVOR_BAL_COMMAND = Admin_Command(
    "set_survivor_bal",
    mod_sp_bal,
    "fs.set_survivor_bal [survivor] [bal] updates a users balance",
)
