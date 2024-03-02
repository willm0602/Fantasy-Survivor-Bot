"""
shows all the players scores

fs.lb
"""

from discord.message import Message

from ...Command import Command
from ...DB import DB
from ..utils import clean_name


async def leaderboard(msg: Message):
    db = DB()
    fps = db.get_all_fantasy_players()
    if len(fps) == 0:
        await msg.channel.send("Nobody signed up yet :(", reference=msg)
        return
    survivors = db.get_all_survivors()
    bets = db.get_all_bets()

    survivor_balances = {}
    for survivor in survivors:
        survivor_balances[survivor["id"]] = survivor["balance"]

    balances = {}
    for fp in fps:
        balances[fp["id"]] = {"name": fp["name"], "id": fp["id"], "bal": fp["bank"]}

    for bet in bets:
        balances[bet["fantasyPlayer"]]["bal"] += (
            bet["amount"] * survivor_balances[bet["survivorPlayer"]]
        )

    positions = []
    for fp in fps:
        data = balances[fp["id"]]
        positions.append((clean_name(data["name"])), data["bal"])
    positions.sort(key=lambda k: k[1], reverse=True)

    res = ""
    for i, pos in enumerate(positions):
        res = res + f"{i+1}) {pos[0]}- {round(pos[1], 3)}\n"
    await msg.channel.send(res, reference=msg)


LB_COMMAND = Command("lb", leaderboard, "fs.lb- shows the leaderboard")
