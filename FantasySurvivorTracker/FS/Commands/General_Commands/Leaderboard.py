'''
shows all the players scores

fs.lb
'''

from ...DB import DB
from ...Command import Command
from discord.message import Message

async def leaderboard(msg: Message):
    db = DB()
    fps = db.get_fantasy_players()
    survivors = db.get_survivors()
    bets = db.get_all_bets()
    
    survivor_balances = {}
    for survivor in survivors:
        survivor_balances[survivor['id']] = survivor['balance']
    
    
    
    balances = {}
    for fp in fps:
        balances[fp['id']] = {
            "name": fp["name"],
            "id": fp["id"],
            "bal": fp["bank"]
        }
        
    
    for bet in bets:
        balances[bet['fantasyPlayer']]['bal']+=bet['amount'] * survivor_balances[bet['survivorPlayer']]
    
    positions = []
    for fp in fps:
        data = balances[fp['id']]
        positions.append((
            data['name'],
            data['bal']
        ))
    positions.sort(
        key=lambda k: k[1], reverse=True
    )
    
    res = ""
    for i, pos in enumerate(positions):
        res = res + f'{i+1}) {pos[0]}- {round(pos[1], 3)}\n'
    await msg.channel.send(res)

LB_COMMAND = Command(
    'lb',
    leaderboard,
    'fs.lb- shows the leaderboard'
)