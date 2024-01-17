"""Restores backed up scores
fs.restore
"""
from ...Command import Admin_Command
from ...DB import DB


async def restore(msg):
    db_client = DB()
    db_client.restore()
    await msg.channel.send(f"successfully restored scores", reference=msg)


RESTORE_COMMAND = Admin_Command(
    "restore",
    restore,
    "fs.restore restores scores",
)
