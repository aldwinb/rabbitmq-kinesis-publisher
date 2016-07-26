from nose.tools import *
from mock import Mock
from nose_parameterized import parameterized
from src import publisher as pub
import boto3
import time


def test_should_execute_declarator():
    channel = Mock()
    channel_declarator = Mock()
    channel_declarator.execute = Mock()
    config = Mock()
    queue_name = 'queue'
    no_ack = False

    pub.start_consume(channel=channel,
                      channel_declarator=channel_declarator,
                      loc_config=config,
                      queue_name=queue_name,
                      no_ack=no_ack)

    channel_declarator.execute.assert_called_with(channel,
                                                  queue_name,
                                                  config)


def test_should_not_fail_if_declarator_is_null():
    channel = Mock()
    channel_declarator = None
    config = Mock()
    queue_name = 'queue'
    no_ack = False

    pub.start_consume(channel=channel,
                      channel_declarator=channel_declarator,
                      loc_config=config,
                      queue_name=queue_name,
                      no_ack=no_ack)
