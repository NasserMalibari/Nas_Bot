
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os
import requests
import datetime
from masters import masters
from collections import namedtuple
import time

mastersBoard = masters()

def get_masters_ladder():
    headers = {
    "X-Riot-Token": KEY
    }

    endpoint = "https://americas.api.riotgames.com/lor/ranked/v1/leaderboards"
    response = requests.get(endpoint, headers=headers)
    
    masters = []

    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        masters = data["players"]
    else:
        print("Request failed with status code:", response.status_code)

    # print(len(masters))
    # print(masters[0:10])
    print(masters[100])
    return masters

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
KEY = os.getenv('API_KEY')

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

print(consumer_key)

class MyClient(discord.Client):
    command_prefix = '!'
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):

        if message.author.id == self.user.id:
            return
        
        print(f'Message from {message.author}: {message.content}')
        
        if ((message.content[0] == '!')):
            await message.channel.send(f"thanks for your command!")

            
# m = get_masters_ladder()
# mastersBoard.add_to_list((m, datetime.datetime.now()))
# print(mastersBoard.get_list()[0][0][0:10])
# print(mastersBoard.get_list()[0][1].strftime("%d/%m/%Y"))

mastersBoard = get_masters_ladder()
player_dictionary = dict()
for player in mastersBoard:
    player_dictionary[player['name']] = player['lp']

m = masters()
m.add_to_masters(mastersBoard)
m.add_to_players(player_dictionary)
# time.sleep(600)
mastersBoard = get_masters_ladder()
player_dictionary = dict()
for player in mastersBoard:
    player_dictionary[player['name']] = player['lp']

m.add_to_masters(mastersBoard)
m.add_to_players(player_dictionary)

# print(f"length of ladder is {len(mastersBoard)}")
m.top_gainers()

# client = MyClient(intents=discord.Intents.all())
# client.run(TOKEN)



# @client.command()
# async def add(ctx, left: int, right: int):
#     """Adds two numbers together."""
#     await ctx.send(left + right)


# description = '''An example bot to showcase the discord.ext.commands extension
# module.
# There are a number of utility commands being showcased here.'''

# intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True

# bot = commands.Bot(command_prefix='?', description=description, intents=intents)


# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user} (ID: {bot.user.id})')
#     print('------')


# @bot.command()
# async def add(ctx, left: int, right: int):
#     """Adds two numbers together."""
#     await ctx.send(left + right)


# @bot.command()
# async def roll(ctx, dice: str):
#     """Rolls a dice in NdN format."""
#     try:
#         rolls, limit = map(int, dice.split('d'))
#     except Exception:
#         await ctx.send('Format has to be in NdN!')
#         return

#     result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
#     await ctx.send(result)


# @bot.command(description='For when you wanna settle the score some other way')
# async def choose(ctx, *choices: str):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.command()
# async def repeat(ctx, times: int, content='repeating...'):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await ctx.send(content)


# @bot.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


# @bot.group()
# async def cool(ctx):
#     """Says if a user is cool.
#     In reality this just checks if a subcommand is being invoked.
#     """
#     if ctx.invoked_subcommand is None:
#         await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


# @cool.command(name='bot')
# async def _bot(ctx):
#     """Is the bot cool?"""
#     await ctx.send('Yes, the bot is cool.')


# bot.run(TOKEN)