"""
fs.manually_deduct
"""


from discord.message import Message

from ...command import Admin_Command
from ...db import DB


async def manually_deduct(msg: Message):
    DB().backup()
    DB().deduct_unspent_points_by_five_percent()
    await msg.channel.send("Deduced all points by 5%")


MANUALLY_DEDUCT_POINTS_COMMAND = Admin_Command(
    "deduct_points",
    manually_deduct,
    "fs.deduct_points - deduct 5% of the unspent points from everyones banks",
)
