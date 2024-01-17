"""
@user the user to be deleted
fs.del_fantasy [@user]
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Admin_Command
from ...DB import DB


async def del_fantasy_player(msg: Message):
    user: Member = msg.mentions[0]
    db = DB()
    db.del_fantasy_player(user)
    channel: TextChannel = msg.channel
    await channel.send(f"successfully removed player {user.display_name}", reference=msg)


DEL_PLAYER_COMMAND = Admin_Command(
    "del_fantasy",
    del_fantasy_player,
    "fs.del_fantasy [@player] deletes a specified fantasy player",
)
