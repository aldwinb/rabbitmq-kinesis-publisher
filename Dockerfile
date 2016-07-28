FROM python:2-alpine

MAINTAINER aldwinb

RUN apk add --update \
    wget \
    jq \
  && rm -rf /var/cache/apk/*

COPY create-aws-sts-token.sh /usr/local/bin/create-aws-sts-token

RUN chmod +x /usr/local/bin/create-aws-sts-token \
  && mkdir /root/.aws \
  && mkdir -p /usr/src/app/config

RUN pip install --upgrade \
    boto3 \
    awscli \
    pika \
    tox

WORKDIR /usr/src/app

COPY ["rmq2k", "entrypoint.sh", "/usr/src/app/"]

ENTRYPOINT ["sh", "entrypoint.sh"]
