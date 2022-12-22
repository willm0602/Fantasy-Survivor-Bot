'''
Signs up a user

fs.signup
'''

from discord.message import Message

from ...Command import Command
from ...DB import DB

async def signup(msg: Message):
    user = msg.author
    db = DB()
    if not db.fp_exists(user):
        db.create_fantasy_player(user)
        await msg.channel.send("Succesfully signed up for the Fantasy League!")
    else:
        raise Exception("Error: You are already signed up!")

SIGNUP_COMMAND = Command(
    'signup', signup, 'fs.signup- signup for the fantasy league'
)
