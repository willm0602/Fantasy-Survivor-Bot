"""
@user the user to be added
fs.new_fantasy [@user]
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...command import Admin_Command
from ...db import DB


async def new_fantasy_player(msg: Message):
    user: Member = msg.mentions[0]
    db = DB()
    db.create_fantasy_player(user)
    channel: TextChannel = msg.channel
    await channel.send(
        f"successfully created new player {user.display_name}", reference=msg
    )


NEW_FANTASY_PLAYER_COMMAND = Admin_Command(
    "new_fantasy",
    new_fantasy_player,
    "fs.new_fantasy [@player] creates a new fantasy player",
)
