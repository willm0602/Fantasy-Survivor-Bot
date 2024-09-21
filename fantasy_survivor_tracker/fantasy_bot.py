import discord

from .fs import COMMANDS

def setup_bot(token):
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f"we have logged in as {client.user.display_name}")

    @client.event
    async def on_message(msg: discord.message.Message):
        content: str = msg.content
        if content.startswith("fs."):
            for command in COMMANDS:
                if command.match(content):
                    res = await command.run(msg)
                    if res is not None:
                        await msg.channel.send(res, reference=msg)
                    return
            await msg.channel.send(f'"{content}" is not a valid command', reference=msg)

    client.run(token)
