from typing import List

from discord.message import Message
from discord.user import User

from ..DB import DB

# parses a discord message to get the command, args and user from it
# used instead of standard "discord py" commands
def parse_message(msg: Message):
    content = msg.content[len("fs.") :]
    data = content.split(" ")
    command = data[0]
    args = data[1:]
    user = msg.author
    return {"command": command, "args": args, "user": user}


# obtains just the arguments from discord
def get_args(msg: Message):
    data = parse_message(msg)
    return data.get("args", [])


# returns a list of tuples with every even-indexed value in the list
# with the value at the index one higher than that (e.g.) if items were
# [0,1,2,3,4,5,6] the function returns [(0,1),(2,3),(4,5)]
def pairwise(items: List):
    pairs = []
    index = 0
    while index < len(items) - 1:
        a = items[index]
        b = items[index + 1]
        pairs.append((a, b))
        index += 2
    return pairs


# checks if a discord user is an admin for the bot
def is_admin(user: User):
    user_id = user.id
    rows = DB().supabase.from_("Admin").select("*").execute().data
    for row in rows:
        if int(row.get("discord_id")) == user_id:
            return True
    return False
