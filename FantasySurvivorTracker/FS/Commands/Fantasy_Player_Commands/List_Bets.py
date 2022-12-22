'''
lets a user view their bets

fs.list_bets [?@user]
'''

from discord.message import Message

from FS.Command import User_Command
from FS.DB import DB


async def list_bets(msg: Message):
    db = DB()
    user = msg.author
    if len(msg.mentions) > 0:
        user = msg.mentions[0]
    id = db.fp_exists(user)
    if id is False:
        if user == msg.author:
            raise Exception('Error: You are not a user')
        raise Exception('Error: this person is not a user')
    bets = db.get_all_bets_for_user(id)
    if len(bets) == 0:
        await msg.channel.send('You have no bets placed')
        return

    bets_list = '\n'.join([
        f"""Bet {bet.get('id')}- {round(db.get_bet_value(bet),2)} for {
            db.get_survivor_player_by_id(
                bet.get('survivorPlayer')
            ).get(
                'name'
            )
        }"""
        for bet in bets
    ])
    await msg.channel.send(bets_list)


LIST_BETS_COMMAND = User_Command(
    'list_bets',
    list_bets,
    'fs.list_bets [?@user] - lets a user view the bets of a user or defaults to themselves'
)
