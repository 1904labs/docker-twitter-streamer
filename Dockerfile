FROM python:3.7.8-slim

# Build Args
ARG BUILD_DATE=None
ARG VCS_REF=None
ARG BUILD_VERSION=None

# Labels.
LABEL maintainer="gjunge@1904labs.com" \
      org.label-schema.schema-version="1.0" \
      org.label-schema.build-date=${BUILD_DATE} \
      org.label-schema.name="1904labs/twitter-streamer" \
      org.label-schema.description="1904labs twitter streamer image" \
      org.label-schema.url="https://1904labs.com/" \
      org.label-schema.vcs-url="https://github.com/1904labs/docker-twitter-streamer" \
      org.label-schema.vcs-ref=${VCS_REF} \
      org.label-schema.vendor="1904labs" \
      org.label-schema.version=${BUILD_VERSION} \
      org.label-schema.docker.cmd="docker run --rm 1904labs/twitter_stream:latest -f '#funny' -k <TWITTER_CONSUMER_KEY> -s <TWITTER_CONSUMER_SECRET> -a <TWITTER_ACCESS_TOKEN> -t <TWITTER_ACCESS_TOKEN_SECRET>"

RUN set -ex && \
  pip install kafka-python==2.0.1 tweepy==3.9.0 boto3==1.13.23

COPY src /opt/bin
RUN set -ex && \
  chmod 755 /opt/bin/twitter_streamer.py

ENTRYPOINT [ "/opt/bin/twitter_streamer.py" ]
