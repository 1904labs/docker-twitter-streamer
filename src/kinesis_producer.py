# stdlib
import os
import sys
import logging

# addlib
import boto3

log = logging.getLogger(__name__)

class KinesisProducer(object):
    def __init__(self):
        self.region = os.environ.get("KINESIS_REGION", 'us-east-1')
        self.api_name = os.environ.get("KINESIS_API_NAME", 'firehose')
        self.stream_name = os.environ.get("KINESIS_STREAM_NAME", 'TwitterStream')
        self.client = boto3.client(self.api_name, region_name=self.region)

    def send(self, partition_key, data):
        return self.client.put_record(
            DeliveryStreamName=self.stream_name, 
            Record={"PartitionKey": partition_key, "Data": data }
        )