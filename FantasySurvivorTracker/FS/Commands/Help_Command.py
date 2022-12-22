
from discord.message import Message

from ..Command import Command

from .Commands import COMMANDS, Admin_Commands, FP_COMMANDS


async def send_help(msg: Message):
    admin_command_details = '**ADMIN_COMMANDS**\n' + '\n'.join([
        command.desc for command in Admin_Commands
    ])
    fp_command_details = '\n\n**USER_COMMANDS**\n' + '\n'.join([
        command.desc for command in FP_COMMANDS
    ])
    other_commands = '\n\n**OTHER_COMMANDS**\n'
    for command in COMMANDS:
        if command not in Admin_Commands and command not in FP_COMMANDS:
            if command.trigger != 'fs.help':
                other_commands+=f'{command.desc}\n'
    res = admin_command_details + fp_command_details + other_commands
    await msg.channel.send(res)

HELP_COMMAND = Command(
    'fs.help',
    send_help,
    None
)