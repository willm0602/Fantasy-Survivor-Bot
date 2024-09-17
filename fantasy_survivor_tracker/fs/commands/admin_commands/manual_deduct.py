"""
fs.manually_deduct
"""


from discord.message import Message

from ...command import AdminCommand
from ...db import DB


async def manually_deduct(msg: Message):
    DB().backup()
    DB().deduct_unspent_points_by_five_percent()
    await msg.channel.send("Deduced all points by 5%", reference=msg)


MANUALLY_DEDUCT_POINTS_COMMAND = AdminCommand(
    "deduct_points",
    manually_deduct,
    "fs.deduct_points - deduct 5% of the unspent points from everyones banks",
)
