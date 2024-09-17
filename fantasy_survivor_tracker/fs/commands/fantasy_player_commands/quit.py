"""
Let's a user quit the fantasy league

fs.quit
"""

from discord.message import Message

from ...command import UserCommand
from ...db import DB
from ...exceptions import CommandInvalidAccessException

async def quit(msg: Message):
    user = msg.author
    db = DB()
    if db.get_registed_user_or_false(user):
        db.del_fantasy_player(user)
        await msg.channel.send("You've left the fantasy league :(", reference=msg)
    else:
        raise CommandInvalidAccessException("Error: You aren't signed up!")


QUIT_COMMAND = UserCommand("quit", quit, "fs.quit- leave the fantasy league")
