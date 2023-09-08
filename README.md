# Fantasy Survivor Tracker

## What is this?

This is a [Discord](https://en.wikipedia.org/wiki/Discord) bot I've developed is designed to facilitate and manage my friend's Fantasy Survivor League, which revolves around the popular reality TV show [Survivor](https://en.wikipedia.org/wiki/Survivor_(American_TV_series)). In this league, participants engage in a friendly competition by placing artificial bets on the performance of the show's contestants. The primary objective is to predict and strategize around the success of individual players throughout the season. This bot allows the administrators for the discord server to manage scores of the Survivor contestants and the people competing in the league.

## How do I run this bot?
1. Clone this repository
2. Install Python
3. Install pipenv by running `pip install pipenv` in your terminal
4. Create a virtual environment by running `pipenv shell` inside the Fantasy-Survivor-Bot directory
5. Get the requirements by runing `pipenv install -r requirements.txt`.
6. Inside Fantasy-Survivor-Bot, create a .env file with the following properties:
   1. DISCORD_TOKEN
   2. supabase_key
   3. supabase_url
7. run `python main.py` from inside the pipenv environment
8. ensure the bot runs properly