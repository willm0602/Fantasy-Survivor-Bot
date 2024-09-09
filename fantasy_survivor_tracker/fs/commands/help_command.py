from discord.message import Message

from ..command import Command
from .commands import COMMANDS, FP_COMMANDS, Admin_Commands
from .utils import is_admin


async def send_help(msg: Message):
    admin_command_details = "**ADMIN_COMMANDS**\n" + "\n".join(
        [command.desc for command in Admin_Commands]
    )
    fp_command_details = "\n\n**USER_COMMANDS**\n" + "\n".join(
        [command.desc for command in FP_COMMANDS]
    )
    other_commands = "\n\n**OTHER_COMMANDS**\n"
    for command in COMMANDS:
        if command not in Admin_Commands and command not in FP_COMMANDS:
            if command.trigger != "fs.help":
                other_commands += f"{command.desc}\n"
    res = ""
    if is_admin(msg.author):
        res += admin_command_details
    res += fp_command_details + other_commands
    await msg.channel.send(res, reference=msg)


HELP_COMMAND = Command("help", send_help, None)
