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

      
# def post_tweet():
#     payload = json.dumps({"text": "Hello World! this is a test tweet"})
#     url, auth = connect_to_oauth(
#         consumer_key, consumer_secret, access_token, access_token_secret
#     )
#     request = requests.post(
#         auth=auth, url=url, data=payload, headers={"Content-Type": "application/json"}
#     )

#     print(request.text)
#     return_data = json.loads(request.text)
#     # print(request.text)
#     print(return_data["data"]["id"])
#     return return_data["data"]["id"]
#     # print(request['id'])
#     # print(type(request['id']))

# def post_reply(tweet_id, reply_status):
#     payload = json.dumps({"text": reply_status, "reply": {"in_reply_to_tweet_id":"1668910101351272448"}})
#     url, auth = connect_to_oauth(
#         consumer_key, consumer_secret, access_token, access_token_secret
#     )
#     request = requests.post(
#         auth=auth, url=url, data=payload, headers={"Content-Type": "application/json"}
#     )

#     print(request.text)

def post_tweet(text, reply=False, reply_id=0):
    
    if (reply == True): 
        payload = json.dumps({"text": text, "reply": {"in_reply_to_tweet_id":str(reply_id)}})
    else:
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




def test_response():
    text = '{"data":{"edit_history_tweet_ids":["1668910101351272448"],"id":"1668910101351272448","text":"Hello World! 4th go"}}'
    response = json.loads(text)
    print (response['data']['id'])

if __name__ == '__main__':
    id = post_tweet("hi, this is a test")
    id2 = post_tweet("reply", True, id)
    # post_reply(1668910101351272448, "a reply!")

