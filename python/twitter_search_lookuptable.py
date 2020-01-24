######################################################################################
### requêtes tweets en fonction d'un user en particulier ou à partir de mots clefs ###
######################################################################################


import tweepy as tw
from tweepy import Cursor
# fichier séparé où se trouve les codes pour se connnecter à l'API Twitter
import twitter_credentials
import pandas as pd
# pour éviter que dataframe ne soit tronqué au moment de l'afficher dans la console de sublime text- more options available###
pd.set_option('expand_frame_repr', False)
import numpy as np
import re
import json

###########################################################
### class permettant la connexion avec l'API de Twitter ###
###########################################################


class TwitterAuthentification:
    def twitter_auth():
        auth = tw.OAuthHandler(twitter_credentials.CONSUMER_KEY,
                               twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.OAUTH_TOKEN,
                              twitter_credentials.OAUTH_TOKEN_SECRET)
        return auth

#############################################################################################################################
### class permettant 3 types de recherches : tweets d'une personne, id d'une personne, requête sur mots clefs ou hashtags ###
#############################################################################################################################


class TwitterSearch:
    def __init__(self):  # connexion API Twitter
        self.auth = TwitterAuthentification.twitter_auth()
        self.api = tw.API(self.auth, wait_on_rate_limit=True,
                          wait_on_rate_limit_notify=True)
        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication")

    """
    écupération des 20 derniers tweets d'une personnes avec création d'une dataframe incluant
    les colonnes 'name', 'tweets', 'creation_date', 'like_count', 'retweeted_count'
    pour permettre une analyse par la suite
    """

    def twitter_get_user_tweets(self, user_name, tweetCount, nomfichier):
        # Calling the user_timeline function with our parameters
        tweets = []
        retweeted_count = []
        like_count = []
        creation_date = []
        name = []

        results = self.api.user_timeline()
        # dans la ligne qui suit je n'utilise pas self.results variable car 1er argument de Cursor ne prend pas de parentheses à la fin)
        for tweet in tw.Cursor(self.api.user_timeline, id=user_name).items(tweetCount):
            tweets.append(tweet.text)
            retweeted_count.append(tweet.retweet_count)
            like_count.append(tweet.favorite_count)
            creation_date.append(tweet.created_at)
            name.append(tweet.user.name)

        df = pd.DataFrame({'name': name, 'tweets': tweets, 'Creation date': creation_date,
                           'nombre de likes': like_count, 'Number if retweets': retweeted_count})

        # indiquer path pour enregistrement du dataframe
        df.to_csv('/Users/geraldbouget/Documents/Git/Python/' +
                  nomfichier + '.csv')

    # récupération du twitter id d'un pseudo
    def get_id(self, user_name):
        self.get_user = self.api.get_user(user_name).id
        return self.get_user

    # requête à partir d'un mot clef ou d'un hashtag ou liste de mots clef/hashtags []
    # donner keyword sous forme keyword #keyword ou sous forme de liste
    # until au format 'YYYY-MM-DD' - count=nombre de tweets par page
    def query(self, keywords, until=None, count=None):
        self.query = keywords
        # Langue
        language = "fr"

        # Calling the user_timeline function with our parameters
        self.results = self.api.search(
            q=self.query, lang=language, until=until, count=None)
        # print(dir(self.results))
        # foreach through all tweets pulled
        for tweet in self.results:
            # printing the text stored inside the tweet object
            print(tweet.user.screen_name, "Tweeted:", tweet.text)

        ### EXEMPLE 2 ###
        # for tweet in api.search(q="Python", lang="en", tweetCount=10):
        #     print("{}:{}".format(tweet.user.name, tweet.text))
        #     pass


################
### REQUETES ###
################

# twitter_user = TwitterSearch()
# tweetuser = twitter_user.twitter_get_user_tweets('@pseudo', NombreTweets, 'NomDataframe.csv')

# requête par mots clefs ou hashtags ou liste de mots clefs/hashtags
twitter_search = TwitterSearch()
a = twitter_search.query('#macron', count=100)
#print(type(a))
