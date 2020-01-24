################################################################
###########SCRIPTS POUR ANALYSER TWEETS VIA TWEEPY##############
###########DATE : 19/01/20 - GERALD BOUGET######################
################################################################


import tweepy as tw
import pandas as pd
# pour éviter que dataframe ne soit tronqué au moment de l'afficher dans la console - more options available###
pd.set_option('expand_frame_repr', False)
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections
import nltk
# nltk.download()

from nltk.corpus import stopwords
import nltk.data
# chargement du tokenizer

from stop_words import get_stop_words
stop_words = get_stop_words('english')

from stop_words import safe_get_stop_words
import re
import networkx
from textblob import TextBlob  # version anglaise
from textblob_fr import PatternTagger, PatternAnalyzer  # version française

import warnings
warnings.filterwarnings("ignore")
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import os


df = pd.read_csv(
    '/Users/geraldbouget/Documents/Git/Python/Twitter/trump_analysis/df_tweet_trump.csv')


class TweetAnalysis:
    df = df

    def clean_characters(self):
        self.df_clean_sentence = df
        self.df_clean_sentence['tweets'] = self.df_clean_sentence['tweets'].apply(
            lambda x: re.sub("[^0-9A-Za-zà-ü\s][\,\:\;\,](^\w')|(\w+:\/\/\S+)", "", x))
        self.df_clean_sentence['tweets'] = self.df_clean_sentence['tweets'].apply(
            lambda x: re.sub("(\w+…)|[,:;,.|@]", "", x))
        return self.df_clean_sentence

    def most_liked_tweets(self):
        ###LES TWEETS LES PLUS LIKÉS###
        self.most_liked_tweets = df[['tweets', 'Creation date', 'nombre de likes', 'Number if retweets']].sort_values(
            by=['nombre de likes'], ascending=False).head(50)
        return self.most_liked_tweets

    def most_retweeted(self):
        ###LES TWEETS LES PLUS RETWEETES###
        most_retweeted = df[['tweets', 'Creation date', 'nombre de likes', 'Number if retweets']].sort_values(
            by=['Number if retweets'], ascending=False).head(50)
        return most_retweeted

    def liste_mots_tweets(self):
        self.liste_mots = []
        self.series_tweets = TweetAnalysis().clean_characters().tweets.apply(
            lambda x: x.lower().split())
        for key, values in self.series_tweets.items():
            self.liste_mots.append(values)
            ### List of all words across tweets ###
        self.liste_mots_onelist = list(itertools.chain(*self.liste_mots))
        return self.liste_mots_onelist

    def stopwords(self):
        self.raw_list = TweetAnalysis().liste_mots_tweets()

        # retrait des mots inutiles avec le mOdule "stop_words" comme point de départ###
        self.liste_stop_word_module = stop_words

        # mise à jour de la liste stop_words à laquelle j'ajoute ma propre liste de stopwords
        #// / A  METTRE À JOUR SOI - MEME // /
        """
        /// ATTENTION: PARFOIS GUILLEMENT DE RAWLIST PAS AU FORMAT NORMAL : 
        FAIRE COPIER COLLET DU MOT RAW LIST DANS MAJ_PERSO_STOP_WORDS ///
        """
        self.maj_perso_stop_words = []

        # stopword liste definitivie
        self.liste_stop_word_def = self.liste_stop_word_module
        for p in self.maj_perso_stop_words:
            if p not in self.liste_stop_word_def:
                self.liste_stop_word_def.append(p)

        # raw liste sans stopwords
        self.clean_list_no_stopwords = [
            r for r in self.raw_list if r not in self.liste_stop_word_def]

        return self.clean_list_no_stopwords

        ### LISTE DES MOTS LES PLUS UTILISES ###
    def most_used_words(self):
        self.wordlist_clean_distr_count = collections.Counter(
            TweetAnalysis().stopwords())
        return self.wordlist_clean_distr_count.most_common(100)

    def wordcloud(self):
        # CONVERSION DES DONNEES EN DICTIONNAIRE UTILISABLE PAR WORDCLOUD
        self.dict_wordcloud = dict(TweetAnalysis().most_used_words())

        # Create and generate a word cloud image:
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").fit_words(
            self.dict_wordcloud).to_file(TweetAnalysis().df.iloc[0, 1] + '.png')  # utilisation methode fitword pour prendre en compte le nombre de mots du dic

        # Display the generated image:
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        return plt.show()

    def sentiment_analysis(self):
        self.df_sentiments = TweetAnalysis().clean_characters()
        self.df_sentiments['tweet_polarity'] = self.df_sentiments['tweets'].apply(
            lambda x: TextBlob(x).sentiment)

        self.df_plot_polarity = self.df_sentiments[[
            'tweet_polarity', 'tweets']]
        self.df_plot_polarity.tweet_polarity = self.df_plot_polarity.tweet_polarity.apply(
            lambda x: x[0])

        fig, ax = plt.subplots(figsize=(8, 6))
        self.df_plot_polarity.hist(bins=[-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1],
                                   ax=ax, color="purple")
        plt.show()
        return plt.show()


trump_analysis = TweetAnalysis()
a = trump_analysis.wordcloud()

#print(TweetAnalysis().df.iloc[0, 1])
