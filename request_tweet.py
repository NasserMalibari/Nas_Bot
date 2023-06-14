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

      
def post_tweet():
    payload = json.dumps({"text": "Hello World! 4th go"})
    url, auth = connect_to_oauth(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    request = requests.post(
        auth=auth, url=url, data=payload, headers={"Content-Type": "application/json"}
    )

    print(request.text)

def post_reply(tweet_id, reply_status):
    payload = json.dumps({"text": reply_status, "reply": {"in_reply_to_tweet_id":"1668910101351272448"}})
    url, auth = connect_to_oauth(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    request = requests.post(
        auth=auth, url=url, data=payload, headers={"Content-Type": "application/json"}
    )

    print(request.text)


def test_response():
    text = '{"data":{"edit_history_tweet_ids":["1668910101351272448"],"id":"1668910101351272448","text":"Hello World! 4th go"}}'
    response = json.loads(text)
    print (response['data']['id'])

if __name__ == '__main__':
    post_reply(1668910101351272448, "a reply!")

