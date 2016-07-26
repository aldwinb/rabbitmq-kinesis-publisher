#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A simple program that forwards messages from RabbitMQ '
                   'queue to an AWS Kinesis stream.',
    'author': 'aldwinb',
    'url': 'https://github.com/aldwinb/rabbitmq-kinesis-publisher',
    'author_email': 'aldwinb@users.noreply.github.com',
    'version': '0.0.1',
    'install_requires': ['pika==0.10.0',
                         'boto3==1.3.1'],
    'packages': ['src'],
    'name': 'rabbitmq-kinesis-publisher'
}

setup(**config)
