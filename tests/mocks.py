class MockArgs(object):
    def __init__(self):
        self.__dict__.update({
            "filter": ["#filter"],
            "consumer_key": "fake_consumer_key",
            "consumer_secret": "fake_consumer_secret",
            "access_token": "fake_access_token",
            "access_token_secret": "fake_access_token_secret"
        })
    
    def __call__(self):
        return [
            "--filter", self.filter[0],
            "--consumer_key", self.consumer_key,
            "--consumer_secret", self.consumer_secret,
            "--access_token", self.access_token,
            "--access_token_secret", self.access_token_secret
        ]


class MockProducer(object):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def send(self, topic, value=None, key=None, headers=None, partition=None, timestamp_ms=None):
        print("Sending (key={} value={} headers={}) to {}".format(key, value, headers, topic))
        return MockFuture(value)


class MockFuture(object):

    def __init__(self, value):
        self.value = value

    def get(self, timeout=None):
        return self.value
