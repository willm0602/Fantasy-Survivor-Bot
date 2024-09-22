import discord

from .fs import COMMANDS
from .fs.command import Command

def get_matching_command(content: str) -> Command | None:
    """Returns the command that matches the message provided"""
    matching_commands = [
        c for c in COMMANDS if c.match(content)
    ]
    if len(matching_commands) > 0:
        return matching_commands[0]
    return None

async def run_command(
    msg: discord.message.Message,
    command: Command | None
):
    if command is None:
        await msg.channel.send(
            f'"{msg.content}" is not a valid command',
            reference=msg
        )
        return
    res = await command.run(msg)
    if res is not None:
        await msg.channel.send(res, reference=msg)

def setup_bot(token):
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f"we have logged in as {client.user.display_name}")

    @client.event
    async def on_message(msg: discord.message.Message):
        content: str = msg.content
        if content.lower().startswith("fs."):
            command = get_matching_command(content)
            await run_command(msg, command)

    client.run(token)
