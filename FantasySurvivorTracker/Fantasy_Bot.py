import discord

from .FS.Command import Command
from .FS.Commands.Commands import COMMANDS
from .FS.Commands.Help_Command import HELP_COMMAND


def setup_bot(token):
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f"we have logged in as {client.user.display_name}")

    @client.event
    async def on_message(msg: discord.message.Message):
        content: str = msg.content
        print("got message", msg)
        if content == "fs.help":
            await HELP_COMMAND.run(msg)
            return
        if content.startswith("fs."):
            for command in COMMANDS:
                if command.match(content):
                    await command.run(msg)
                    return

    client.run(token)
