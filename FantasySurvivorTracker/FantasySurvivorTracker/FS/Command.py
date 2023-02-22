import sys
import traceback
from email import message
from typing import Callable

from discord.message import Message

from .Commands.utils import is_admin
from .DB import DB

DEFAULT_DESCRIPTION = "A Fantasy Survivor Command"


class Command:
    def __init__(self, trigger: str, action: Callable, desc: str = DEFAULT_DESCRIPTION):
        self.trigger = trigger
        self.action = action
        self.desc = desc

    def match(self, msg: str):
        if not msg.startswith("fs."):
            return False
        return msg[len("fs.") :].startswith(self.trigger)

    async def run(self, msg: Message):
        if not msg.author.bot:
            try:
                await self.action(msg)
            except Exception as e:
                await msg.channel.send(e)

                # https://stackoverflow.com/a/28836286
                error_class = e.__class__.__name__
                detail = e.args[0] if len(e.args) else "no details found"
                cl, ex, tb = sys.exc_info()
                line = traceback.extract_tb(tb)[-1][1]
                traceback.print_tb(tb)
                print(
                    f"{error_class} exception on line {line} of file: {detail}\n{e.args}"
                )


class Admin_Command(Command):
    async def run(self, msg: Message):
        if not msg.author.bot:
            user = msg.author
            if is_admin(user):
                await super().run(msg)
                return
            else:
                await msg.channel.send(
                    "Error: you must be an admin to run this command"
                )


class User_Command(Command):
    async def run(self, msg: Message):
        user = msg.author
        if not user.bot:
            db = DB()
            if db.fp_exists(user):
                await super().run(msg)
                return
            else:
                await msg.channel.send(
                    "Error: you need to be a user to run this command"
                )
