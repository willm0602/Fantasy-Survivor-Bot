"""
Signs up a user

fs.signup
"""

from discord.message import Message
from discord.utils import get

from ...Command import Command
from ...DB import DB


class MockRole:
    def __init__(self, id):
        self.id = int(id)


async def signup(msg: Message):
    user = msg.author
    db = DB()
    if not db.fp_exists(user):
        db.create_fantasy_player(user)
        season_role = MockRole(db.get_setting("seasonRoleID"))
        not_playing_role = MockRole(db.get_setting('notSignedUpID'))
        await user.add_roles(season_role)
        await user.remove_roles(not_playing_role)
        await msg.channel.send("Succesfully signed up for the Fantasy League!")
    else:
        raise Exception("Error: You are already signed up!")


SIGNUP_COMMAND = Command("signup", signup, "fs.signup- signup for the fantasy league")
