"""
fs.list_settings
"""


from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message

from ...Command import Admin_Command
from ...DB import DB
from ..utils import parse_message


async def list_settings(msg: Message):
    db = DB()
    res = ''
    for key, val in db.get_all_settings().items():
        res = res + f'{key}: {val}\n'
    await msg.channel.send(res)

LIST_SETTINGS_COMMAND = Admin_Command(
    "list_settings",
    list_settings,
    "fs.list_settings - list all of the settings placed",
)
