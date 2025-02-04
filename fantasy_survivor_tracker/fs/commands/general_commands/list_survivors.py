"""
lists all survivors and their current scores

fs.list_survivors
"""

from discord.message import Message

from ...command import Command
from ...db import DB


async def list_survivors(msg: Message):
    db = DB()
    survivors = db.get_all_survivors()
    survivors.sort(key=lambda s: s["name"])
    if len(survivors):
        res = "\n".join([f"{s['name']}" for s in survivors])
        await msg.channel.send(res, reference=msg)
    else:
        await msg.channel.send("No Survivors Yet", reference=msg)


LIST_SURVIVORS_COMMAND = Command(
    "list_survivors", list_survivors, "fs.list_survivors- shows all survivors"
)
