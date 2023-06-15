import json
import boto3
import os
from masters import get_masters_ladder, get_player_dictionary, get_player_dict_fictional

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
    clear_table(table1)

    count = 0
    for d in data:
        table1.put_item(Item={"username":d['username'], "points":d["points"]})
        if (count % 100 == 0):
            print(f"{count} items copied")
        count += 1
    print(f"2nd arg has {get_db_size(table1)} items")


# return two lists of size 5 each:
# biggest gainers and biggest losers
def get_biggest_differences(table0, table1):
    return_payload = dict()
    # return_payload["gainers"] =
    # return_payload["losers"] =
    differences = {}
    

    pass


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")
    day0_table_name = os.environ["DAY0_TABLE"]
    day1_table_name = os.environ["DAY1_TABLE"]

    day0_table = dynamodb.Table(day0_table_name)
    day1_table = dynamodb.Table(day1_table_name)

    # no data has been entered
    if (get_db_size(day1_table) == 0):
        print("table 1 has  no items!")
        # put masters data in
        count = 0
        players = get_player_dictionary()
        for user, points in players.items():
            # print(user +  ' ' + points)
            day1_table.put_item(Item={"username":user, "points":points})
            count += 1
            if (count % 100 == 0):
                print(f"{count} players processed")


        # return
    # elif (get_db_size(day0_table) != get_db_size(day1_table)):
    #     # we have only 1 day of data

    #     print("elif")
    #     # copy day1 into day0
    #     copy_items(day1_table, day0_table)

    #     # rewrite day 1
    #     players = get_player_dict_fictional(get_player_dictionary())
    #     for user, points in players.items():
    #         # print(user +  ' ' + points)
    #         day1_table.put_item(Item={"username":user, "points":points})
    #         count += 1
    #         if (count % 100 == 0):
    #             print(f"{count} players processed")
    
    if (event['user'] == "nas_local"):
        pass
        
        

    # return { "message" : message }

# def lambda_handler_test_use(event, context):
    
#     # fictional data
#     day0_masters = {'p1':100, "p2":50}
#     day1_masters = {'p1': 50, "p2": 250, "p3":14, "p4":0}

#     dynamodb = boto3.resource("dynamodb")
#     day0_table_name = os.environ["DAY0_TABLE"]
#     day1_table_name = os.environ["DAY1_TABLE"]

#     day0_table = dynamodb.Table(day0_table_name)
#     day1_table = dynamodb.Table(day1_table_name)

#     # no data has been entered
#     if (get_db_size(day1_table) == 0):
#         print("table 1 has  no items!")
#         # put masters data in
#         count = 0
#         for user, points in day0_masters.items():
#             day1_table.put_item(Item={"username":user, "points":points})


#         # return
#     elif (get_db_size(day0_table) == 0):
#         # move day 1 to day 0

#         # clear day 0
#         clear_table(day0_table)

#         # copy 
#         print("about to copy")

#         # copy day1 masters into day 0 masters
#         copy_items(day1_table, day0_table)

#         # FIXME
#         # day0_table = day1_table
#         print("size of day 0 is now " + str(get_db_size(day0_table)))

#         # clear_table(day1_table_name)
#         for user, points in day1_masters.items():
#             day1_table.put_item(Item={"username":user, "points":points})

#     print(get_db_size(day0_table))
#     print(get_db_size(day1_table))


if __name__ == "__main__":
    event = {"user" : "nas_local"}
    dynamodb = boto3.resource('dynamodb')
    os.environ["DAY0_TABLE"] = "day0"
    os.environ["DAY1_TABLE"] = "day1"

    day0_table = dynamodb.Table(os.environ["DAY0_TABLE"])
    day1_table = dynamodb.Table(os.environ["DAY1_TABLE"])
    
    # print(get_db_size(day0_table))
    # print(get_db_size(day1_table))
    lambda_handler(event, None)
    # print(get_db_size(day0_table))
    # print(get_db_size(day1_table))
    # # get_all_items(day0_table)
    # clear_tables()
    # clear_table(day1_table)
    # copy_items(day1_table, day0_table)

