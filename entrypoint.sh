#!/usr/bin/env bash

$(create-aws-sts-token -c /root/.aws/$1 -t $2)
if [ "$?" -eq "0" ]; then
  python -u publisher.py
fi