"""
    This file has all functions communicating with the 
    player_icons database.

    Players can opt in to have an emoji associated with their username in the tweets

"""

import boto3


dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "player_icons"



def add_player(username, icon, server):
    """
        Add player 
    
    """
    pass


