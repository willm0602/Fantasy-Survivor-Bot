"""
lists all survivors and their current scores

fs.list_survivors
"""

from discord.message import Message

from ...Command import Command
from ...DB import DB


async def list_survivors(msg: Message):
    db = DB()
    survivors = db.get_survivors()
    survivors.sort(key=lambda k: k["balance"])
    res = "\n".join([f"{s['name']} - {s['balance']}" for s in survivors])
    await msg.channel.send(res)


LIST_SURVIVORS_COMMAND = Command(
    "list_survivors", list_survivors, "fs.list_survivors- shows all survivors"
)
