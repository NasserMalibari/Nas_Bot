import datetime
from collections import deque
import requests
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('API_KEY')

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
    # print(masters[100])
    return masters

def get_player_dictionary():
    player_dictionary = dict()
    # print(get_masters_ladder()[0])

    for player in get_masters_ladder():
        player_dictionary[player['name']] = int(player['lp'])

    return player_dictionary

def get_player_dict_fictional(player_dict):
    pass
    # i = player_dict['Kuako']
    fict_dict = player_dict

    fict_dict['Kuako'] = fict_dict['Kuako'] - 100
    fict_dict['Dolmant'] = fict_dict['Dolmant'] + 150

    return fict_dict


"""
The following class represents a list of 'snapshots' 
of the masters leaderboard (as a list), combined with the time the snapshot was taken (datetime)
"""
class masters:

    def __init__(self):
        # each item is a dictionary
        # most recent entries on left side of deque
        self.masters = deque()
        self.players = deque()

    def get_deque(self):
        return self.masters
    
    def get_players(self):
        return self.players

    def add_to_masters(self, item):
        if (len(self.masters) >= 30):
            self.masters.pop()
        self.masters.appendleft(item)
    
    def add_to_players(self, item):
        if (len(self.masters) >= 30):
            self.players.pop()
        self.players.appendleft(item)

    # calculate inflation
    def inflation():
        pass

    # top LP Gainers for the past day
    def top_gainers(self):
        # create dictionary of player differences using dict comprehension
        differences = {}

        # 
        for name, lp in self.players[1].items():
            differences[name] = -lp
    
        for name in self.players[1].keys():
            # print(f"subtracting {self.players[-1].get(name)} from {name}")
            differences[name] = differences[name] + self.players[0].get(name)
        
        max_pair = max(differences.items(), key=lambda x: x[1])
        print(max_pair)
        return max_pair

    # top LP Losers
    def top_losers(self):
        differences = {}

        # 
        for name, lp in self.players[1].items():
            differences[name] = -lp
    
        for name in self.players[1].keys():
            # print(f"subtracting {self.players[-1].get(name)} from {name}")
            differences[name] = differences[name] + self.players[0].get(name)
        
        min_pair = min(differences.items(), key=lambda x: x[1])
        print(min_pair)
        return min_pair

if __name__ == '__main__':
    get_player_dict_fictional(get_player_dictionary())
