'''
Let's a user split their bank between 

fs.split *[survivor name]
'''

from discord.message import Message

from FS.Command import Command, User_Command
from FS.DB import DB

from ..utils import get_args


async def split(msg: Message):
    user = msg.author
    db = DB()
    user_id = db.fp_exists(user)
    args = get_args(msg)
    if len(args) == 0:
        raise Exception('no arguments provided')
    for name in args:
        if not db.survivor_exists(name):
            raise Exception(f'{name} is not a survivor')
    bank = db.get_balance(
        user_id
    )
    bet_per_player = bank / len(args)
    for name in args:
        db.create_bet(
            user, name, bet_per_player
        )
    await msg.channel.send('successfully split')

SPLIT_COMMAND = User_Command(
    'split',
    split,
    'fs.split [survivor_names]* - splits your remaining bank between each name'
)
