"""
survivor_name - the name of the survivor as we have them in list_bets
alias - the alias to use for the survivor
fs.add_alias [survivor_name] [alias]
"""

from discord.message import Message

from ...command import AdminCommand
from ...db import DB
from ..utils import get_args
from ...exceptions import CommandInputException
from ...exceptions import ModelInstanceDoesNotExist

async def add_alias(msg: Message):
    args = get_args(msg)
    if len(args) != 2:
        raise CommandInputException('Proper usage: add_alias <survivor_name> <alias>')

    (survivor_name, alias) = args

    db = DB()
    try:
        db.add_alias(survivor_name, alias)
    except ModelInstanceDoesNotExist:
        await msg.channel.send(f'No Survivor with name {survivor_name} exists')

    await msg.channel.send(f'Added alias for {alias}')

ADD_ALIAS_COMMAND = AdminCommand(
    "add_alias",
    add_alias,
    "fs.add_alias [survivor_name] [alias] adds an alias for the survivor",
)
