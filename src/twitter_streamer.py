#!/usr/bin/env python3

# stdlib
import os
import sys
import logging
import argparse

# include path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# addlib
from tweepy_stream import TweepyStream

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

def get_producer():
    if os.getenv("KAFKA_SERVICE_HOST", False):
        from kafka_producer import KafkaProducer
        return KafkaProducer()
    elif os.getenv("KAFKA_BOOTSTRAP_SERVER", False):
        from kafka_producer import KafkaProducer
        return KafkaProducer()
    elif os.getenv("KINESIS_STREAM_NAME", False):
        from kinesis_producer import KinesisProducer
        return KinesisProducer()
    else:
        from tweepy_stream import StdoutProducer
        return StdoutProducer()

def check_args(args):
    if not args.filter:
        twitter_api_filter = os.environ.get("TWITTER_API_FILTER")
        if twitter_api_filter:
            args.filter = [twitter_api_filter]
        else:
            args.filter = ['#']
    if not args.consumer_key:
        raise Exception("Missing twitter api consumer key")
    if not args.consumer_secret:
        raise Exception("Missing twitter api consumer secret")
    if not args.access_token:
        raise Exception("Missing twitter api access token")
    if not args.access_token_secret:
        raise Exception("Missing twitter api access token secret")
    return vars(args)

def get_args(incoming = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', action='append')
    parser.add_argument('-k', '--consumer_key', default=os.environ.get("TWITTER_CONSUMER_KEY"))
    parser.add_argument('-s', '--consumer_secret', default=os.environ.get("TWITTER_CONSUMER_SECRET"))
    parser.add_argument('-a', '--access_token', default=os.environ.get("TWITTER_ACCESS_TOKEN"))
    parser.add_argument('-t', '--access_token_secret', default=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))
    args = parser.parse_args(incoming)
    args.producer = get_producer()
    return check_args(args)

if __name__ == "__main__":
    args = get_args(sys.argv[1:])
    stream = TweepyStream(**args).filter(track=args['filter'])

