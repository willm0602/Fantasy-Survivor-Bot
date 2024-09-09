"""Backs up survivor scores

fs.backup
"""
from ...command import Admin_Command
from ...db import DB


async def backup(msg):
    await msg.channel.send("Starting backup...", reference=msg)
    db_client = DB()
    db_client.backup()
    await msg.channel.send("successfully backed up scores", reference=msg)


BACKUP_COMMAND = Admin_Command(
    "backup",
    backup,
    "fs.backup backs up scores",
)
