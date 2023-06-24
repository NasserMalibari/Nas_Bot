import datetime
from collections import deque
import requests
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('API_KEY')
DEV = os.getenv('DEV_KEY')

# server is one of 'am' 'eu' 'ap'
def get_masters_ladder(server):
    headers = {
    "X-Riot-Token": KEY
    }

    if (server not in ['am', 'eu', 'ap']):
        raise ValueError("server not specified correctly")

    if (server == 'am'):
        endpoint = "https://americas.api.riotgames.com/lor/ranked/v1/leaderboards"
    elif (server == 'eu'):
        endpoint = "https://europe.api.riotgames.com/lor/ranked/v1/leaderboards"
    elif (server == 'ap'):
        endpoint = "https://sea.api.riotgames.com/lor/ranked/v1/leaderboards"
    
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

# server is one of 'am' 'eu' 'ap'
def get_player_dictionary(server):
    player_dictionary = dict()
    # print(get_masters_ladder()[0])

    for player in get_masters_ladder(server):
        player_dictionary[player['name']] = int(player['lp'])

    return player_dictionary

def get_player_dict_fictional(player_dict):
    pass
    # i = player_dict['Kuako']
    fict_dict = player_dict

    fict_dict['Kuako'] = fict_dict['Kuako'] - 100
    fict_dict['Dolmant'] = fict_dict['Dolmant'] + 150

    return fict_dict

def lp_requirements(server):
    p_list = get_masters_ladder(server)

    rank1 = 0
    rank10 = 0
    rank25 = 0 
    rank50 = 0
    rank100 = 0

    if (len(p_list) >= 1):
        rank1 = int(p_list[0]['lp'])
    if (len(p_list) >= 10):
        rank10 = int(p_list[9]['lp'])
    if (len(p_list) >= 25):
        rank25 = int(p_list[24]['lp'])
    if (len(p_list) >= 50):
        rank50 = int(p_list[49]['lp'])
    if (len(p_list) >= 100):
        rank100 = int(p_list[99]['lp'])

    return {1:rank1, 10:rank10, 25:rank25, 50: rank50, 100:rank100}


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

    print(lp_requirements("am"))
    # # get_player_dictionary('eu')
    # headers = {
    # "X-Riot-Token": DEV
    # }

    # endpoint = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/MajiinBae'

    # response = requests.get(endpoint, headers=headers)

    # if response.status_code == 200:
    #     data = response.json()
    #     # Process the data as needed
    #     # masters = data["players"]
    #     print(data)
    # else:
    #     print("Request failed with status code:", response.status_code)

    # print(KEY)
