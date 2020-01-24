#######################################################################
### class permettant la connexion avec l'API de Twitter en streaming ##
################DATE 17/01/20 - GERALD BOUGET##########################
#######################################################################


import tweepy as tw
from tweepy import Stream, StreamListener
import twitter_credentials
import pandas as pd
# pour éviter que dataframe ne soit tronqué au moment de l'afficher dans la console de sublime text- more options available###
pd.set_option('expand_frame_repr', False)
import numpy as np
import re
import json

# override tweepy.StreamListener to add logic to on_status


class TwitterAuthentification:
    def twitter_auth():
        auth = tw.OAuthHandler(twitter_credentials.CONSUMER_KEY,
                               twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.OAUTH_TOKEN,
                              twitter_credentials.OAUTH_TOKEN_SECRET)
        return auth


class MyStreamListener(tw.StreamListener):
    def on_status(self, status):
        with open('sexeducation2_tweets.csv', 'a') as tf:
            pd.DataFrame({
                'tweet': [status.text],
            }).to_csv(tf, header=False)

    def on_data(self, data):
        # print(data)
        # print data
        with open('fetched_tweets.txt', 'a') as tf:
            tf.write(data)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
            # returning non-False reconnects the stream, with backoff.


class mystreamSearch:
    def __init__(self):

        self.api = tw.API(TwitterAuthentification.twitter_auth(), wait_on_rate_limit=True,
                          wait_on_rate_limit_notify=True)
        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication")

    def stream_filter(self, filter):

        self.myStreamListener = MyStreamListener()

        self.myStream = tw.Stream(
            auth=TwitterAuthentification.twitter_auth(), listener=self.myStreamListener)

        # choosing language !
        self.myStream.filter(languages=["fr"], track=filter, is_async=True)


mystream = mystreamSearch()
sexeducation = mystream.stream_filter(['#sexeducation'])
