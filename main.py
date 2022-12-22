# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands
from FantasySurvivorTracker import Fantasy_Bot

token = os.environ["DISCORD_TOKEN"]
Fantasy_Bot.setup_bot(token)
