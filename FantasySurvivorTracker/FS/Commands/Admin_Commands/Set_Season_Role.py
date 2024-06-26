"""
fs.set_season_role [@SEASON_ROLE]
"""
import re

from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Admin_Command
from ...DB import DB
from ..utils import parse_message


async def set_season_role(msg: Message):
    db = DB()
    mentions = re.findall("<@&.*>", msg.content)
    role_id = mentions[0][3:-1]
    db.set_setting("seasonRoleID", role_id)
    await msg.channel.send(f"Set role to <@&{role_id}>", reference=msg)


SET_SEASON_ROLE_COMMAND = Admin_Command(
    "set_season_role",
    set_season_role,
    "fs.set_season_role @role - sets the role for the current season",
)
