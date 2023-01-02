"""
@name the name of the survivor player
fs.new_survivor [@name]
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Admin_Command
from ...DB import DB
from ..utils import parse_message


async def new_survivor_player(msg: Message):
    data = parse_message(msg)
    args = data.get("args")
    if len(args) < 1:
        raise Exception("Error: Survivor player name must be specified")
    name = args[0]
    db_client = DB()
    if not db_client.survivor_exists(name):
        db_client.create_survivor_player(name)
        await msg.channel.send(f"Succesfully created new Survivor Player {name}")
    else:
        raise Exception("Error: Player Already Exists")


NEW_SURVIVOR_PLAYER_COMMAND = Admin_Command(
    "new_survivor",
    new_survivor_player,
    "fs.new_survivor [survivor] creates a new survivor player",
)
