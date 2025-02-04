"""
fs.set_not_signed_up_role [@SEASON_ROLE]
"""
import re

from discord.message import Message

from ...command import AdminCommand
from ...db import DB


async def set_not_signed_up_role(msg: Message):
    db = DB()
    mentions = re.findall("<@&.*>", msg.content)
    role_id = mentions[0][3:-1]
    db.set_setting("notSignedUpID", role_id)
    await msg.channel.send(f"Set role to <@&{role_id}>", reference=msg)


SET_NOT_SIGNED_UP_ROLE = AdminCommand(
    "set_not_signed_up_role",
    set_not_signed_up_role,
    "fs.set_not_signed_up_role @role - sets the role for users not playing",
)
