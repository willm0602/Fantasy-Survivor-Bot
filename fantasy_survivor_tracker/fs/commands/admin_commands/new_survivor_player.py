"""
@name the name of the survivor player
fs.new_survivor [@name]
"""


from discord.message import Message

from ...command import Admin_Command
from ...db import DB
from ..utils import parse_message
from ...exceptions import CommandInputException

async def new_survivor_player(msg: Message):
    data = parse_message(msg)
    args = data.get("args")
    if len(args) < 1:
        raise CommandInputException("Error: Survivor player name must be specified")
    name = args[0]
    db_client = DB()
    if not db_client.get_survivor_by_name_or_false(name):
        db_client.create_survivor_player(name)
        await msg.channel.send(
            f"successfully created new Survivor Player {name}", reference=msg
        )
    else:
        raise CommandInputException("Error: Player Already Exists")


NEW_SURVIVOR_PLAYER_COMMAND = Admin_Command(
    "new_survivor",
    new_survivor_player,
    "fs.new_survivor [survivor] creates a new survivor player",
)
