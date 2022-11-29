import tweepy
import time
from kafka import KafkaProducer

bearer_token= r"AAAAAAAAAAAAAAAAAAAAACddhQEAAAAAJf6G0ZqwhPI46bXY7WvUjtlmio4%3DqYBBgJ3mkE49mJj0WNvrfbXCg7lbiPldBelynrrQkCEYrlyKTH"
api_key = "sIZmnRFGSXlruVfOWFOev6eGX"
api_secret = "6HggNXL2llVLVxNzXEpqMwLXAfu2uLoLoO2JWzk7RWHHykwlED"
access_token = '1571982292217733121-FpSCelJc2NeTaYnqiV7TxlnHNUahv8'
access_token_secret = 'XNqPSbfxfjPMKpF34789QpLutjvfIkrtjWWf0PDxrEgvX'

tweepy.Client(bearer_token,api_key,api_secret,access_token,access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key,api_secret,access_token,access_token_secret)
api = tweepy.API(auth)

topic_name = "mqtt_attack"
topic_name = "testing"
search_terms = ["IoT-attack", "IoT-crime"]
search_terms = [
    "slowite",
    "bruteforce",
    "flood",
    "malformed",
    "dos"
]
producer = KafkaProducer(bootstrap_servers='localhost:9092')


class MyStream(tweepy.StreamingClient):

    def on_status(self, status):
        print(status.text)
        
    def on_connect(self):
        print("connected")
    
    def on_tweet(self,tweet):
        if tweet.referenced_tweets == None:
            print (tweet.text)
            producer.send(topic_name,tweet.text.encode('utf-8'))
            time.sleep(1.5)
            
            
stream = MyStream(bearer_token=bearer_token)

for term in search_terms:
    stream.add_rules(tweepy.StreamRule(term))   # filter rule - search term

stream.filter(tweet_fields=["referenced_tweets"])
