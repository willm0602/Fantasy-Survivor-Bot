# This file contains types we can use to simulate a discord message without
# actually needing to send discord messages so we can run automated tests

from typing import List

import discord
from FS.Commands.Commands import COMMANDS
from FS.Commands.Help_Command import HELP_COMMAND


class FakeUser:
    """Class to simulate a discord user"""

    id: int
    username: str
    bot = False

    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username


BOT = FakeUser(0, "Fantasy Survivor Bot")
BOT.bot = True


class FakeChannel:
    id = 1
    name = "Fake Channel"
    messages: List["FakeMesssage"]

    def __init__(self, messages: List["FakeMessage"] = []):
        self.messages = messages

    def send(self, message: str):
        self.messages.append(FakeMesssage(self, message))

    def get_contents(self):
        return "\n".join([message.content for message in self.messages])


class FakeMesssage:
    channel: FakeChannel
    content: str
    author: FakeUser
    mentions: List[FakeUser]

    def __init__(self, channel: FakeChannel, content: str, author: FakeUser = BOT):
        self.channel = channel
        self.content = content
        self.author = author
        self.mentions = []


def make_fake_message(content: str, author: FakeUser = BOT):
    channel = FakeChannel()
    return FakeMesssage(channel, content, author)


def run(msg: FakeMesssage) -> FakeChannel:
    content: str = msg.content
    print("got message", msg)
    if content == "fs.help":
        HELP_COMMAND.run(msg)
        return
    if content.startswith("fs."):
        for command in COMMANDS:
            if command.match(content):
                command.run(msg)
                return msg.channel
