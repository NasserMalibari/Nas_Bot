import requests
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.environ['API_KEY']

# server is one of 'am' 'eu' 'ap'
def get_masters_ladder(server):
    """ return leaderboard from RIOT API

        Args:
            server (string): One of "am", "eu" or "ap"

        Returns:
            List of dictionaries with keys:
                "name" -> string
                "rank" -> int
                "lp"   -> float 

        Example:
            >>> get_masters_ladder("am")
            [{"name":Naś , "rank":1, "lp": 1001}, ... ]
    """

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

    return masters
    
# server is one of 'am' 'eu' 'ap'  
def get_country(username, server):
    """ Get the country of origin if player submitted theirs to runeterra.ar 
    
    Args:
        username (string): name of the player
        server   (string): server the player plays on, one of ["am","eu","ap"]

    Returns:
        country code (string): two letter country code if player submitted country,
                               empty string if player didn't upload

    Example:
        >>> get_country("Naś", "am")
        AU
    
    Raises:
        ValueError: If 'server' is not one of ['am', 'eu', 'ap']

    """

    if (server not in ['am', 'eu', 'ap']):
        raise ValueError("server not specified correctly")
    
    endpoint = ""

    if (server == 'am'):
        endpoint = f"https://runeterra.ar/api/users/get/country/americas/{username}"
    elif (server == 'eu'):
        endpoint = f"https://runeterra.ar/api/users/get/country/europe/{username}"
    elif (server == 'ap'):
        endpoint = f"https://runeterra.ar/api/users/get/country/apac/{username}"

    resp = requests.get(endpoint)
    
    if (resp.status_code == 200):
        print("success!")
        print(resp.text)
        return get_flag_emoji(resp.text)
    else:
        print("failure")
        return ""


# server is one of 'am' 'eu' 'ap'
def get_player_dictionary(server):
    """
        Generate a python dictionary of the leaderboard gathered by RIOT API

        Args:
            server (string): one of 'am', 'eu' or 'ap' indicating the server of the returned leaderboard
    
        Returns:
            dictionary with key: username (string), value: points (int)

        Example:
            >>> get_player_dictionary("am")
            {"Naś": 1001 , 
              ...
            }
    """

    player_dictionary = dict()

    for player in get_masters_ladder(server):
        player_dictionary[player['name']] = int(player['lp'])

    return player_dictionary

def get_player_dict_fictional(player_dict):
    '''  Creates a 'fictional' leaderboard dictionary for testing '''

    # i = player_dict['Kuako']
    fict_dict = player_dict

    fict_dict['Kuako'] = fict_dict['Kuako'] - 100
    fict_dict['Dolmant'] = fict_dict['Dolmant'] + 150

    return fict_dict
    
def lp_requirements(server):
    """ Return dictionary that specifies how much lp is needed for a subset of rank thresholds

    Args: 
        server (list): one of "am", "eu", "ap"
    
    Returns:
        Dictionary with keys of 1, 10, 25, 50, 100 (int),
        and values of lp (points) required (int)
    
    """
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

        

# Turns out country flags are just the two letter country code put together as emoji's
# note: flag emoji's do not appear on windows systems
def get_flag_emoji(country_code):
    """ Returns the specified emoji for given country code """

    
    flag_offset = 127397
    uppercase_country_code = country_code.upper()
    emoji_flag = ""
    
    for char in uppercase_country_code:
        emoji_flag += chr(ord(char) + flag_offset)
    
    return emoji_flag

if __name__ == '__main__':
    get_masters_ladder('eu')
