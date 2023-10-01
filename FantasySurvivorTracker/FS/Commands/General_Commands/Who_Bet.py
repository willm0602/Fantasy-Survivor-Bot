"""
lists all survivors and the total number of points on each of them

fs.stats
"""

from discord.message import Message

from ...Types import FantasyPlayer
from ...Command import Command
from ...DB import DB
from ..utils import get_args

from typing import TypedDict, Set, Dict, List

async def who_bet(msg: Message):
    db = DB()
    args = get_args(msg)
    if len(args) == 0:
        await msg.channel.send('No arguments provided')
        raise ValueError
    survivor_name = args[0]

    survivor = db.get_survivor_by_name_or_false(survivor_name)
    if survivor is False:
        await msg.channel.send(f'{survivor_name} is not a survivor')
        raise ValueError

    all_bets = db.get_all_bets()
    bets: Dict[str, float] = {}
    for bet in all_bets:
        bet_amount = bet['amount']
        if bet['survivorPlayer'] != survivor['id']:
            continue
        fp_id = bet['fantasyPlayer']
        fp: FantasyPlayer = db.get_registed_user_by_id_or_false(fp_id)
        if fp:
            fp_name = fp['name']
            if fp_name in bets:
                bets[fp_name]+=bet_amount
            else:
                bets[fp_name]=bet_amount
    sorted_bets = sorted(
        bets.items(),
        key = lambda bet: bet[1],
        reverse=True
    )
    _msg = '\n'.join([f'{bet[0]}- {bet[1]}' for bet in sorted_bets])
    await msg.channel.send(_msg)

WHO_BET_COMMAND = Command(
    "who_bet_on", who_bet, "fs.who_bet_on [survivor]- shows how much each player bet on a survivor"
)
