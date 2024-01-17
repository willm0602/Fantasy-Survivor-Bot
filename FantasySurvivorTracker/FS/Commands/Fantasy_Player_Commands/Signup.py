"""
Signs up a user

fs.signup
"""

from discord.message import Message
from discord.utils import get

from ...Command import Command
from ...DB import DB


class MockRole:
    """We need to pass in an object w/ an id to simulate the role that we're
    modifying"""

    def __init__(self, id):
        self.id = int(id)

    def __bool__(self):
        return self.id is not None


async def signup(msg: Message):
    user = msg.author
    db = DB()
    if not db.get_registed_user_or_false(user):
        db.create_fantasy_player(user)
        season_role = MockRole(db.get_setting("seasonRoleID"))
        not_playing_role = MockRole(db.get_setting("notSignedUpID"))
        if season_role:
            await user.add_roles(season_role)
        if not not_playing_role:
            await user.remove_roles(not_playing_role)
        await msg.channel.send("successfully signed up for the Fantasy League!", reference=msg)
    else:
        raise Exception("Error: You are already signed up!")


SIGNUP_COMMAND = Command("signup", signup, "fs.signup- signup for the fantasy league")
