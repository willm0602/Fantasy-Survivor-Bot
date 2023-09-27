"""
Let's a user quit the fantasy league

fs.quit
"""

from discord.message import Message

from ...Command import Command, User_Command
from ...DB import DB


async def quit(msg: Message):
    user = msg.author
    db = DB()
    if db.get_registed_user_or_false(user):
        db.del_fantasy_player(user)
        await msg.channel.send("You've left the fantasy league :(")
    else:
        raise Exception("Error: You aren't signed up!")


QUIT_COMMAND = User_Command("quit", quit, "fs.quit- leave the fantasy league")
