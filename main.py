#!/usr/bin/env python3

import os

import discord
import dotenv
from discord.ext import commands

from FantasySurvivorTracker import Cron, Fantasy_Bot

# loads environment variables on local if developing
dotenv.load_dotenv(".env")

token = os.environ["DISCORD_TOKEN"]
Fantasy_Bot.setup_bot(token)
