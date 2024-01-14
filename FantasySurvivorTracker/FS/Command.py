from datetime import datetime
import sys
import traceback
from email import message
from typing import Callable
from .Types import CommandRun
import traceback
import json

from discord.message import Message

from .Commands.utils import get_args, is_admin, list_bets
from .DB import DB

DEFAULT_DESCRIPTION = "A Fantasy Survivor Command"


def safe_locals():
    _locals = locals()
    _safe_locals = {}
    for key, val in _locals.items():
        try:
            _safe_locals[key] = str(val)
            continue
        except:
            pass
    return _safe_locals


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
        start_time = datetime.now()
        error_msg = ""
        if not msg.author.bot:
            try:
                await self.action(msg)
                was_successful = True
                end_time = datetime.now()
                duration = (end_time - start_time).seconds
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
                was_successful = False
                end_time = datetime.now()
                duration = (end_time - start_time).microseconds / 1000000
                error_msg = (
                    str(traceback.format_exception(e))
                    + "\nLOCALS: "
                    + json.dumps(safe_locals(), indent=4)
                )
            command_run: "CommandRun" = {
                "time_ran": start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "user_ran": msg.author.display_name,
                "time_to_complete": duration,
                "errored": not was_successful,
                "trigger": self.trigger,
                "arguments": get_args(msg),
                "traceback": error_msg,
            }
            DB().log_command_to_db(command_run)


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
            if db.get_registed_user_or_false(user):
                await super().run(msg)
                return
            else:
                await msg.channel.send(
                    "Error: you need to be a user to run this command"
                )


class Bet_Command(User_Command):
    async def run(self, msg: Message):
        await super().run(msg)
        if DB().get_registed_user_or_false(msg.author):
            await list_bets(msg)
