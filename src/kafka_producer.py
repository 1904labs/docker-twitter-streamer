# stdlib
import os
import logging

# addlib
import kafka

log = logging.getLogger(__name__)

class KafkaProducer(kafka.KafkaProducer):

    def __init__(self, **configs):
        """
        """
        #Allow available settings to be retrieved from env variables
        for key in self.DEFAULT_CONFIG:
            envkey = "KAFKA_" + key.upper()
            if os.getenv(envkey, False):
                configs[key] = os.getenv(envkey)
        # If bootstrap server is not set
        if 'bootstrap_servers' not in configs:
            configs['bootstrap_servers'] = self._get_kafka_service_endpoint()
        super().__init__(**configs)

    def _get_kafka_service_endpoint(self):
        """
        Create the bootserver string from the kubernetes variables used in 
        the bitnami helm chart (https://bitnami.com/stack/kafka/helm)
        """
        kafka_service_host = os.getenv("KAFKA_SERVICE_HOST", False)
        kafka_service_port = os.getenv("KAFKA_SERVICE_PORT", 2181)
        if kafka_service_host:
            return kafka_service_host + ":" + kafka_service_port
        else:
            return self.DEFAULT_CONFIG['bootstrap_servers']
