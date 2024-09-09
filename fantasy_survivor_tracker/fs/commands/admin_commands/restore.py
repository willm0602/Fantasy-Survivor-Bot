"""Restores backed up scores
fs.restore
"""
from ...command import Admin_Command
from ...db import DB


async def restore(msg):
    db_client = DB()
    db_client.restore()
    await msg.channel.send("successfully restored scores", reference=msg)


RESTORE_COMMAND = Admin_Command(
    "restore",
    restore,
    "fs.restore restores scores",
)
