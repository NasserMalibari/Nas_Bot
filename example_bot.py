
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
