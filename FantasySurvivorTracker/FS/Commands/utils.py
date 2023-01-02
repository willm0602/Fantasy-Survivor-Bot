from typing import List
from discord.message import Message
from discord.user import User


def parse_message(msg: Message):
    content = msg.content[len("fs.") :]
    data = content.split(" ")
    command = data[0]
    args = data[1:]
    user = msg.author
    return {"command": command, "args": args, "user": user}


def get_args(msg: Message):
    data = parse_message(msg)
    return data.get("args", [])


def pairwise(items: List):
    pairs = []
    index = 0
    while index < len(items) - 1:
        a = items[index]
        b = items[index + 1]
        pairs.append((a, b))
        index += 2
    return pairs


ADMIN_IDS = [192465045161115649, 422857053254713364]


def is_admin(user: User):
    return user.id in ADMIN_IDS
