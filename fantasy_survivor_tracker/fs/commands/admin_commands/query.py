
"""
@query the query to run
fs.query <query>
"""


from discord.message import Message

from ...command import AdminCommand
from ...db import DB

async def query_command(msg: Message):
    query = msg.content[len('fs.query '):]
    resp = DB().supabase.rpc(query, {}).execute()
    await msg.channel.send(resp.json())

QUERY_COMMAND = AdminCommand(
    "query",
    query_command,
    "fs.query <QUERY> - execute a db query"
)
