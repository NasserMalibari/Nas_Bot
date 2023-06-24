import json
import boto3
import os
from masters import get_player_dictionary
import heapq
from datetime import date
import requests
import json
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1

url = "https://api.twitter.com/2/tweets"

load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

def connect_to_oauth(consumer_key, consumer_secret, acccess_token, access_token_secret):
   url = "https://api.twitter.com/2/tweets"
   auth = OAuth1(consumer_key, consumer_secret, acccess_token, access_token_secret)
   return url, auth

      
def post_tweet(text, reply=False, reply_id=0):
    payload = json.dumps({"text": text})
    url, auth = connect_to_oauth(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    request = requests.post(
        auth=auth, url=url, data=payload, headers={"Content-Type": "application/json"}
    )

    print(request.text)
    return_data = json.loads(request.text)
    return return_data["data"]["id"]

dynamodb = boto3.client('dynamodb')


def clear_tables():

    day0_table = dynamodb.Table(os.environ["DAY0_TABLE"])
    day1_table = dynamodb.Table(os.environ["DAY1_TABLE"])


    if (get_db_size(day0_table) != 0):
        clear_table(day0_table)

    if (get_db_size(day1_table) != 0):
        clear_table(day1_table)

def clear_table(table):
    response = table.scan(
        ProjectionExpression='username'  # Specify the primary key attribute(s) of your table
    )

    print("started clearing table")

    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression='username',  # Specify the primary key attribute(s) of your table
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        print("extending")
        items.extend(response['Items'])

    count = 0
    for item in items:
        table.delete_item(
            Key=item
        )
        count += 1
        if (count % 100 == 0):
            print(f"{count} items deleted")

def get_db_size(table):

    return table.scan(
        Select='COUNT'
    )['Count']

def all_items(table):
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    print(data)

# copy table = into table 1
def copy_items(table0, table1):
    response = table0.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table0.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        print("extending data")
    
    print("clearing 2nd arg")
    # clear_table(table1)

    count = 0
    for d in data:
        table1.put_item(Item={"username":d['username'], "points":d["points"]})
        if (count % 100 == 0):
            print(f"{count} items copied")
        count += 1
    print(f"2nd arg has {get_db_size(table1)} items")

# turns a list of dicts to dict
# negative = True, will negate all values of list1 into final dict
def list_to_dict(list1, negative = False):
    player_dictionary = dict()
    # print(type(player['points']))

    for player in list1:
        if (negative):
            player_dictionary[player['username']] = - int(float(player['points']))
        else:
            player_dictionary[player['username']] = + int(float(player['points']))
        # print(int(float(player['points'])))

    return player_dictionary


def post_lor_tweet(server, gainers, losers):
    if (server not in ['am', 'eu', 'ap']):
        raise ValueError("server not specified correctly")
    
    server_name = "APAC"
    if(server == 'am'):
        server_name = "AMERICAS"
    elif(server == "eu"):
        server_name = "EUROPE"
    losers_text=(f"{server_name} - {date.today()}\n"
          f"TOP 5 Unluckiest Master Players\n\n"
          f"🥇. {losers[0][0]} [{losers[0][1]}]\n"
          f"🥈. {losers[1][0]} [{losers[1][1]}]\n"
          f"🥉. {losers[2][0]} [{losers[2][1]}]\n"
        )
    
    for index, val in enumerate(losers[3:], start=4):
        losers_text += f"{index}. {val[0]} [{val[1]}]\n"
    print(losers_text)

    winners_text=(f"{server_name} - {date.today()}\n"
          f"TOP 5 Master Players that gained more LP\n\n"
          f"🥇. {gainers[0][0]} [{gainers[0][1]}]\n"
          f"🥈. {gainers[1][0]} [{gainers[1][1]}]\n"
          f"🥉. {gainers[2][0]} [{gainers[2][1]}]\n"
        )
    
    for index, val in enumerate(gainers[3:], start=4):
        winners_text += f"{index}. {val[0]} [{val[1]}]\n"
    print(winners_text)

    id = post_tweet(winners_text)
    id = post_tweet(losers_text, True, id)


    pass

# return two lists of size 5 each:
# biggest gainers and biggest losers
def get_biggest_differences(table0, table1):
    return_payload = dict()

    differences = {}


    # Perform the scan operation to retrieve all items
    response_0 = table0.scan()
    response_1 = table1.scan()

    # Retrieve the items from the response
    items_0 = response_0['Items']
    items_1 = response_1['Items']

    # turn items (list) into 1 dictionary
    day0_dict = list_to_dict(items_0, True)
    day1_dict = list_to_dict(items_1, False)

    # add dicts together
    for user, lp in day0_dict.items():
        differences[user] = lp
    
    for user in day0_dict.keys():
        differences[user] = differences[user] + day1_dict[user]

    max_values = heapq.nlargest(5, differences, key=differences.get)
    # print(max_values)

    min_values = heapq.nsmallest(5, differences, key=differences.get)
    # print(min_values)

    max_items = [ (player, differences[player]) for player in max_values ]
    min_items = [ (player, differences[player]) for player in min_values ]

    # print(max_items)

    return_payload["gainers"] = max_items

    return_payload["losers"] = min_items

    return return_payload

    # pass


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")

    post_tweet = event['post_tweet']

    if (event['server'] == "am"):
        day0_table_name = os.environ["DAY0_TABLE_AM"]
        day1_table_name = os.environ["DAY1_TABLE_AM"]
    elif (event['server'] == "eu"):
        day0_table_name = os.environ["DAY0_TABLE_EU"]
        day1_table_name = os.environ["DAY1_TABLE_EU"]
    elif (event['server'] == "ap"):
        day0_table_name = os.environ["DAY0_TABLE_AP"]
        day1_table_name = os.environ["DAY1_TABLE_AP"]
    else:
        raise ValueError("am, eu or ap not specified")
    

    day0_table = dynamodb.Table(day0_table_name)
    day1_table = dynamodb.Table(day1_table_name)

    # no data has been entered
    if (get_db_size(day1_table) == 0):
        print("table 1 has  no items!")
        # put masters data in
        count = 0
        players = get_player_dictionary(event['server'])
        for user, points in players.items():
            # print(user +  ' ' + points)
            day1_table.put_item(Item={"username":user, "points":points})
            count += 1
            if (count % 100 == 0):
                print(f"{count} players processed")

        return
    else:
        # we have at least one day of data

        # copy day1 into day0
        copy_items(day1_table, day0_table)

        count = 0
        players = get_player_dictionary(event['server'])
        for user, points in players.items():
            day1_table.put_item(Item={"username":user, "points":points})
            count += 1
            if (count % 100 == 0):
                print(f"{count} players processed")


    # post tweet logic
    if (post_tweet == False):
        return

    if (get_db_size(day0_table) >= 50 and get_db_size(day1_table) >= 50):
        # post tweet
        diffs = get_biggest_differences(day0_table, day1_table)
        # post_lor_tweet(event['server'], diffs["gainers"], diffs["losers"])
        # print("posted the tweet")
        pass


if __name__ == "__main__":
    # event = {"server" : "am", "post_tweet":False}
    dynamodb = boto3.resource('dynamodb')
    os.environ["DAY0_TABLE_AM"] = "day0"
    os.environ["DAY1_TABLE_AM"] = "day1"
    os.environ["DAY0_TABLE_EU"] = "day0eu"
    os.environ["DAY1_TABLE_EU"] = "day1eu"
    os.environ["DAY0_TABLE_AP"] = "day0ap"
    os.environ["DAY1_TABLE_AP"] = "day1ap"

    day0_table = dynamodb.Table(os.environ["DAY0_TABLE_AM"])
    day1_table = dynamodb.Table(os.environ["DAY1_TABLE_AM"])
    # return_val = get_biggest_differences(day0_table, day1_table)
    # print(return_val["gainers"])
    # print(get_db_size(day0_table))
    # print(get_db_size(day1_table))
    # lambda_handler(event, None)

    event = {"server" : "eu", "post_tweet":False}
    lambda_handler(event, None)

    event = {"server" : "ap", "post_tweet":False}
    lambda_handler(event, None)
    # print(get_db_size(day0_table))
    # print(get_db_size(day1_table))

    # diffs = get_biggest_differences(day0_table, day1_table)
    # post_lor_tweet(event['server'], diffs["gainers"], diffs["losers"])
    # print(get_db_size(day0_table))
    # print(get_db_size(day1_table))
    # # get_all_items(day0_table)
    # clear_tables()
    # clear_table(day1_table)
    # copy_items(day1_table, day0_table)

