# stdlib
import os
import sys
import logging

# addlib
import boto3

log = logging.getLogger(__name__)

class RecordAccumulator(object):

    def __init__(self):
        self.limit = 20
        self.container = []
    
    def empty(self):
        result, self.container = self.container, []
        return result

    def full(self):
        return True if len(self.container) >= self.limit else False
    
    def append(self, record):
        self.container.append(record)
        
class KinesisProducer(object):
    def __init__(self, api_name, region_name, stream_name):
        self.client = boto3.client(api_name, region_name=region_name)
        self.stream_name = stream_name
        self.accumulator = RecordAccumulator()

    def send(self, topic, data):
        self.accumulator.append({
            "Data": data.encode('utf-8'),
        })
        if self.accumulator.full():
            return self.client.put_record_batch(
                Records=self.accumulator.empty(),
                DeliveryStreamName=self.stream_name, 
            )
        else:
            return True