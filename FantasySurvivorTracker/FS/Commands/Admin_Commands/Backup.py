"""Backs up survivor scores

fs.backup
"""
from ...Command import Admin_Command
from ...DB import DB

async def backup(msg):
    db_client = DB()
    db_client.backup()
    await msg.channel.send(f"Succesfully backed up scores")
    
BACKUP_COMMAND = Admin_Command(
    "backup",
    backup,
    "fs.backup backs up scores",
)
