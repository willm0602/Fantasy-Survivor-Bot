"""
lists all survivors and their current scores

fs.list_survivors
"""

from discord.message import Message

from ...Command import Command
from ...DB import DB


async def list_survivors(msg: Message):
    db = DB()
    survivors = db.get_all_survivors()
    survivors.sort(key=lambda s: s["name"])
    if len(survivors):
        res = "\n".join([f"{s['name']}" for s in survivors])
        await msg.channel.send(res)
    else:
        await msg.channel.send("No Survivors Yet")


LIST_SURVIVORS_COMMAND = Command(
    "list_survivors", list_survivors, "fs.list_survivors- shows all survivors"
)
