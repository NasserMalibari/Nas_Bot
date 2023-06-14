import json
import boto3
import os


def lambda_handler(event, context):

    user = event['user']

    visit_count = 0

    #create dynamo db client
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    # response = table.get_item(Key={"user":user})
    response = table.get_item(Key={"user": user})
    if "Item" in response:
        visit_count = response["Item"]["count"]

    visit_count += 1

    table.put_item(Item={"user":user, "count":visit_count})

    # message = 'Hello ' + user + '!'
    message = f"Hello {user}! You have visited this page {visit_count} times."

    return { "message" : message }

if __name__ == "__main__":
    event = {"user" : "nas_local"}
    os.environ["TABLE_NAME"] = "visit-count-table"
    print(lambda_handler(event, None))