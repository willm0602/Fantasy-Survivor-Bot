from typing import List

from discord.message import Message
from discord.user import User

from ..exceptions import CommandInputException, CommandInvalidAccessException
from ..db import DB


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


async def list_bets(msg: Message):
    db = DB()
    user = msg.author
    if len(msg.mentions) > 0:
        user = msg.mentions[0]
    id = db.get_registed_user_or_false(user)
    if id is False:
        if user == msg.author:
            raise CommandInvalidAccessException("Error: You are not a user")
        raise CommandInputException("Error: this person is not a user")
    bets = db.get_all_bets_for_user(id)
    if len(bets) == 0:
        await msg.channel.send("You have no bets placed", reference=msg)
        return
    total_bet_amounts = {}
    for bet in bets:
        survivor = bet.get("survivorPlayer")
        if survivor not in total_bet_amounts:
            total_bet_amounts[survivor] = 0
        total_bet_amounts[survivor] += db.get_bet_value(bet)
    response = ""
    for survivor, total_bet in total_bet_amounts.items():
        survivor_name = db.get_survivor_player_by_id_or_false(survivor).get("name")
        response += f"{total_bet:.2f} for {survivor_name}\n"
    await msg.channel.send(response, reference=msg)


def clean_name(name: str) -> str:
    """Cleans the name so it can be readable in discord"""
    UNDERSCORE_LOOKALIKE = "﹍"
    # we need to replace underscores with a readable character
    name = name.replace("_", UNDERSCORE_LOOKALIKE)
    name = name.title()
    return name
