"""
lets a user view their bets

fs.list_bets [?@user]
"""

from discord.message import Message

from ...Command import User_Command
from ...DB import DB


async def list_bets(msg: Message):
    db = DB()
    user = msg.author
    if len(msg.mentions) > 0:
        user = msg.mentions[0]
    id = db.get_registed_user_or_false(user)
    if id is False:
        if user == msg.author:
            raise Exception("Error: You are not a user")
        raise Exception("Error: this person is not a user")
    bets = db.get_all_bets_for_user(id)
    if len(bets) == 0:
        await msg.channel.send("You have no bets placed")
        return
    total_bet_amounts = {}
    for bet in bets:
        survivor = bet.get("survivorPlayer")
        if survivor not in total_bet_amounts:
            total_bet_amounts[survivor] = 0
        total_bet_amounts[survivor] += db.get_bet_value(bet)
    response = ""
    for survivor, total_bet in total_bet_amounts.items():
        survivor_name = db.get_survivor_player_by_id_or_false(survivor).get(
            "name"
        )
        response += f"{total_bet:.2f} for {survivor_name}\n"
    await msg.channel.send(response)


LIST_BETS_COMMAND = User_Command(
    "list_bets",
    list_bets,
    "fs.list_bets [?@user] - lets a user view the bets of a user or defaults to themselves",
)
