"""
@user the user to be deleted
fs.del_survivor [@user]
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Admin_Command
from ...DB import DB
from ..utils import parse_message


async def del_survivor(msg: Message):
    data = parse_message(msg)
    args = data.get("args")
    if len(args) < 1:
        raise Exception("Error: Survivor player name must be specified")
    name = args[0]
    db_client = DB()
    if db_client.survivor_exists(name):
        db_client.delete_survivor_player(name)
        await msg.channel.send(f"Succesfully deleted Survivor Player {name}")
    else:
        raise Exception("Error: Player Doesn't Exists")


DEL_SURVIVOR_COMMAND = Admin_Command(
    "del_survivor",
    del_survivor,
    "fs.del_survivor [survivor player name] deletes a specified survivor player",
)
