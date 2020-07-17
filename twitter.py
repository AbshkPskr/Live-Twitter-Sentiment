# import dash
# from dash.dependencies import Input, Output, State
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly
# import random
# import plotly.graph_objs as go
# from collections import deque
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from unidecode import unidecode
from textblob import TextBlob
import re
import pandas

# app = dash.Dash('Twitter Sentiment analyser')

import sqlite3

# api = tweepy.API(auth)


class listener(StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            # tweet = (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", data['text']).split()))
            time_ms = data['timestamp_ms']
            analysis = TextBlob(tweet)
            sentiment = analysis.sentiment.polarity
            print(time_ms)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?,?,?)",(time_ms,tweet,sentiment))
            conn.commit()
        except KeyError as e:
            # print(str(e))
            pass
        return(True)

    def on_error(self, status):
        print(status)

c=1
conn=1
def get_tweets():
    global conn
    conn = sqlite3.connect('twitter.db')
    global c
    c = conn.cursor()

    def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        conn.commit()

    create_table()

    consumer_key = 'dD4i6dIp7mQLLALBd26rHw'
    consumer_secret = 'kSdjITYWdMGkK0RkfNtMNejuiOaOrqZtezOzFJ2NzQ'
    access_key = '1945980420-WLnsskYxAdHM411Fnqry7Oubz0NVT2juwP6pySo'
    access_secret = 'Xwg1KbAKQzqeWvIXcxAE2FE2xMJpxhgdEuRH0N6MCJBN9'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["a","e","i","o","u"],stall_warnings=True)
    
# get_tweets()