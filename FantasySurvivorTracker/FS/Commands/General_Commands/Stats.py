"""
lists all survivors and the total number of points on each of them

fs.stats
"""

from discord.message import Message

from ...Command import Command
from ...DB import DB

from typing import TypedDict, Set, Dict, List

class SurvivorScore(TypedDict):
    players: Set[int]
    total_amount: float
    name: str

async def stats(msg: Message):
    db = DB()
    survivors = db.get_all_survivors()
    survivor_stats: Dict[int, SurvivorScore] = {}
    for survivor in survivors:
        survivor_stats[survivor['id']] = {
            'players': set(),
            'total_amount': 0,
            'name': survivor['name']
        }
    bets = db.get_all_bets()
    for bet in bets:
        bet_amount = bet['amount']
        survivor_id = bet['survivorPlayer']
        existing_data = survivor_stats[survivor_id]
        existing_data['players'].add(bet['fantasyPlayer'])
        existing_data['total_amount']+=bet_amount
        survivor_stats[survivor_id] = existing_data

    survivors: List['SurvivorScore'] = sorted(
        survivor_stats.values(),
        key=lambda survivor: survivor['total_amount'],
        reverse=True
    )
    result = '\n'.join([
        f'{s["name"]} had {len(s["players"])} players bet a total of {s["total_amount"]:.2f}' for s in survivors
    ])
    await msg.channel.send(result)

STATS_COMMAND = Command(
    "stats", stats, "fs.stats- show how much each Survivor has been bet on"
)
