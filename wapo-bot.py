#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, tweepy, json, time

auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_KEY"], os.environ["ACCESS_SECRET"])
api = tweepy.API(auth)

FOLLOW_ID = 2467791 # Follow @washingtonpost

class WaPoListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        parsed = json.loads(data)
        print(parsed['user']['id'])
        if parsed['user']['id'] == FOLLOW_ID:
            try:
                api.retweet(parsed['id_str'])
                time.sleep(60)
            except Exception as err:
                print(err)
                pass

    def on_error(self, status_code):
        if status_code == 420:
            return False

wapo_listener = WaPoListener()
wapo_stream = tweepy.Stream(auth = api.auth, listener = wapo_listener, timeout=60)
wapo_stream.filter(follow = [str(FOLLOW_ID)])

