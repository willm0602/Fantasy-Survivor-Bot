#!/usr/bin/env python3

import os

import dotenv

from fantasy_survivor_tracker import cron, setup_bot

# loads environment variables on local if developing
dotenv.load_dotenv(".env")

token = os.environ["DISCORD_TOKEN"]
print(f"USING TOKEN {token}")
setup_bot(token)
