
"""
fs.list_tables
"""


from discord.message import Message

from ...command import AdminCommand
from ...db import DB


async def list_tables(msg: Message):
    db = DB()
    tables = db.supabase.rpc('get_all_tables', {}).execute()
    res = ""
    for table in tables:
        res = res + f"{table}\n"
    await msg.channel.send(res, reference=msg)


LIST_TABLES_COMMAND = AdminCommand(
    "list_tables",
    list_tables,
    "fs.list_tables- list all of the tables in the database",
)
