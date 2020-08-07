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
        self.full = 100
        self.container = []
    
    def empty(self):
        result, self.container = self.container, []
        return result

    def full(self):
        return (len(self.container) >= self.limit)
    
    def append(self, record):
        self.container.append(record)
        
class KinesisProducer(object):
    def __init__(self):
        self.region = os.environ.get("KINESIS_REGION", 'us-east-1')
        self.api_name = os.environ.get("KINESIS_API_NAME", 'firehose')
        self.stream_name = os.environ.get("KINESIS_STREAM_NAME", 'TwitterStream')
        self.accumulator = RecordAccumulator()
        self.client = boto3.client(self.api_name, region_name=self.region)

    def send(self, partition_key, data):
        self.accumulator.append({
            "PartitionKey": partition_key, 
            "Data": data.encode('utf-8'),
        })
        if self.accumulator.full():
            return self.client.put_records(
                Records=self.accumulator.empty(),
                DeliveryStreamName=self.stream_name, 
            )