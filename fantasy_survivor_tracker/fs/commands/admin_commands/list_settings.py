"""
fs.list_settings
"""


from discord.message import Message

from ...command import AdminCommand
from ...db import DB


async def list_settings(msg: Message):
    db = DB()
    res = ""
    for key, val in db.get_all_settings().items():
        res = res + f"{key}: {val}\n"
    await msg.channel.send(res, reference=msg)


LIST_SETTINGS_COMMAND = AdminCommand(
    "list_settings",
    list_settings,
    "fs.list_settings - list all of the settings placed",
)
