import datetime

"""
The following class represents a list of 'snapshots' 
of the masters leaderboard (as a list), combined with the time the snapshot was taken (datetime)
"""
class masters:

    def __init__(self):
        self.masters = []
        self.my_datetime = datetime.datetime.now()

    def get_list(self):
        return self.masters

    def get_datetime(self):
        return self.my_datetime

    def add_to_list(self, item):
        self.masters.append(item)

    # calculate inflation
    def inflation():
        pass

    # top LP Gainers
    def top_gainers(num):
        pass

    # top LP Losers
    def top_losers(num):
        pass

