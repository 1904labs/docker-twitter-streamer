# stdlib
import os
import sys
import logging

from tweepy import Stream, StreamListener, OAuthHandler

log = logging.getLogger(__name__)

class TweepyStream(Stream):

    def __init__(self, **kwargs):
        producer = kwargs.pop("producer", StdoutProducer())
        filteron = kwargs.pop("filter", "#")
        authkeys = ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']
        authargs = {key: kwargs.pop(key) for key in authkeys}

        # add listener, remove producer
        if 'listener' not in kwargs:
            kwargs['listener'] = TweepyStreamListener(producer, filteron)

        # add auth remove login info
        if 'auth' not in kwargs:
            kwargs['auth'] = self._get_auth(**authargs)

        super().__init__(**kwargs)

    def _get_auth(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

class TweepyStreamListener(StreamListener):

    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic

    def on_data(self, data):
        self.producer.send(self.topic, data)
        return True

    def on_error(self, status):
        print("Error: " + str(status))

class StdoutProducer(object):

    def send(self, topic, data):
        print(f"{topic}: {data}\n")
        return True