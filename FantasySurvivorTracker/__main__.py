import dotenv

from os import environ, path

from Fantasy_Bot import setup_bot

# loads env file if run locally
if path.isfile("../.env"):
    dotenv.load_dotenv("../.env")

token = environ["discord_token"]
setup_bot(token)
