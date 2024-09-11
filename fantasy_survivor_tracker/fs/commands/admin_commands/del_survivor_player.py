"""
@user the user to be deleted
fs.del_survivor [@user]
"""


from discord.message import Message

from ...command import Admin_Command
from ...db import DB
from ..utils import parse_message
from ...exceptions import CommandInputException


async def del_survivor(msg: Message):
    data = parse_message(msg)
    args = data.get("args")
    if len(args) < 1:
        raise CommandInputException("Error: Survivor player name must be specified")
    name = args[0]
    db_client = DB()
    if db_client.get_survivor_by_name_or_false(name):
        db_client.delete_survivor_player(name)
        await msg.channel.send(
            f"successfully deleted Survivor Player {name}", reference=msg
        )
    else:
        raise CommandInputException("Error: Player Doesn't Exists")


DEL_SURVIVOR_COMMAND = Admin_Command(
    "del_survivor",
    del_survivor,
    "fs.del_survivor [survivor player name] deletes a specified survivor player",
)
