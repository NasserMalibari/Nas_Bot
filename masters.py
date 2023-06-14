import datetime
from collections import deque

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
