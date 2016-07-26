#!/usr/bin/env bash

if [ "$#" -eq "2" ]; then
  $(create-aws-sts-token -c /root/.aws/$1 -t $2)
fi

if [ "$?" -eq "0" ]; then
  python -u publisher.py /usr/src/app/config/config.ini
fi