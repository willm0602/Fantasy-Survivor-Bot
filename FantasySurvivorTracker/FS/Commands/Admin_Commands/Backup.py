"""Backs up survivor scores

fs.backup
"""
from ...Command import Admin_Command
from ...DB import DB


async def backup(msg):
    await msg.channel.send(f"Starting backup...", reference=msg)
    db_client = DB()
    db_client.backup()
    await msg.channel.send(f"successfully backed up scores", reference=msg)


BACKUP_COMMAND = Admin_Command(
    "backup",
    backup,
    "fs.backup backs up scores",
)
