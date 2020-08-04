#!/usr/bin/env python

import sys
import pytest
from tests.mocks import *
from src.tweepy_stream import (
    StdoutProducer,
)
from src.twitter_streamer import (
    check_args,
    get_args,
    get_producer,
)


def arg_asserts(args):
    assert args['filter'] == ['#filter']
    assert args['consumer_key'] == 'fake_consumer_key'
    assert args['consumer_secret'] == 'fake_consumer_secret'
    assert args['access_token'] == 'fake_access_token'
    assert args['access_token_secret'] == 'fake_access_token_secret'

def test_check_args():
    arg_asserts(get_args(MockArgs()()))  

def test_get_args():
    arg_asserts(check_args(MockArgs()))

def test_get_args_env(monkeypatch):
    monkeypatch.setenv('TWITTER_API_FILTER', '#filter')
    monkeypatch.setenv('TWITTER_CONSUMER_KEY', 'fake_consumer_key')
    monkeypatch.setenv('TWITTER_CONSUMER_SECRET', 'fake_consumer_secret')
    monkeypatch.setenv('TWITTER_ACCESS_TOKEN', 'fake_access_token')
    monkeypatch.setenv('TWITTER_ACCESS_TOKEN_SECRET', 'fake_access_token_secret')
    arg_asserts(get_args())

def test_get_producer(monkeypatch):
    producer = get_producer()
    assert isinstance(producer, object)