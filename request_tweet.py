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

# payload = json.dumps({
#   "text": "Hello World! 2nd go"
# })
# headers = {
#   'Content-Type': 'application/json',
#   'Authorization': 'OAuth oauth_consumer_key="5Ei4W98mWvpv5Fi50meQHBMbP",oauth_token="1668880777919217665-uhlJdxa3f4i8TldYM94RxZgWzh2lxy",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1686729062",oauth_nonce="BVATMdl5mTt",oauth_version="1.0",oauth_signature="lAjYFUD0T%2FsdR%2FFvrKGCSHWo22U%3D"'
# }

      
def post_tweet():
    payload = json.dumps({"text": "Hello World! 3rd go"})
    url, auth = connect_to_oauth(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    request = requests.post(
        auth=auth, url=url, data=payload, headers={"Content-Type": "application/json"}
    )
    print(request.text)


if __name__ == '__main__':
    post_tweet()

