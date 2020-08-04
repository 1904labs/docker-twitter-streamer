FROM python:3.7.8-slim


RUN set -ex && \
  pip install kafka-python==2.0.1 tweepy==3.8.0 boto3==1.13.23

COPY src /opt/bin
RUN set -ex && \
  chmod 755 /opt/bin/twitter_streamer.py

ENTRYPOINT [ "/opt/bin/twitter_streamer.py" ]
