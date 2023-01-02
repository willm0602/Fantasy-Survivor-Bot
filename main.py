import dotenv
import os
import discord
from discord.ext import commands
from FantasySurvivorTracker import Fantasy_Bot
from FantasySurvivorTracker import Cron

# loads environment variables on local if developing
dotenv.load_dotenv(".env")

token = os.environ["DISCORD_TOKEN"]
Fantasy_Bot.setup_bot(token)
