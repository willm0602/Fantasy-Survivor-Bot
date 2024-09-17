"""
@?error - optionally pass in the ID of the error to read about
"""
from discord.message import Message

from ..._types import CommandRun
from ...command import AdminCommand
from ...db import DB
from ..utils import parse_message


def format_err(err: CommandRun) -> str:
    args = err["arguments"]
    res = f"{err['id']} - {err['user_ran']} has run fs.{err['trigger']}"
    if args:
        res += f" with arguments args {args}"
    return res


async def read_error_log(msg: Message):
    data = parse_message(msg)
    args = data.get("args")

    error_id = None
    if len(args) > 0:
        try:
            error_id = int(args[0])
        except ValueError:
            await msg.channel.send("Error id must be an integer", reference=msg)
            return

    if error_id is not None:
        error: "CommandRun" = DB().get_error_by_id(error_id)
        if error is None:
            await msg.channel.send(f"{error_id} is not a valid error id", reference=msg)
        else:
            await msg.channel.send(error["traceback"], reference=msg)
    else:
        error_items = []
        for error in DB().get_all_errors()[:10]:
            error_items.append(format_err(error))
        res = "\n".join(error_items)
        await msg.channel.send(res, reference=msg)


READ_ERROR_LOG = AdminCommand(
    "read_error",
    read_error_log,
    "fs.read_error [?id] read information about an error",
)
