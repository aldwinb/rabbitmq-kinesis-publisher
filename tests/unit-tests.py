from nose.tools import *
from mock import Mock
from src import (publisher as pub, declarator as dec)


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


class TestTopicsDeclarator(object):

    def test_should_bind_routing_keys_correctly(self):
        channel = Mock()
        channel.exchange_declare = Mock()
        exchange = ''
        queue_name = ''
        routing_keys = 'key1,key2'
        config = Mock()
        config.get = Mock(side_effect=lambda *x: {
            ('rabbitmq', 'exchange'): exchange,
            ('rabbitmq', 'routing keys'): routing_keys,
            ('rabbitmq', 'prefetch count'): 1}[x])
        d = dec.TopicsDeclarator()

        d.execute(channel=channel, queue_name=queue_name, config=config)

        channel.queue_bind.assert_any_call(exchange=exchange,
                                           queue=queue_name,
                                           routing_key='key1')
        channel.queue_bind.assert_any_call(exchange=exchange,
                                           queue=queue_name,
                                           routing_key='key2')

    def test_should_set_prefetch_count_if_value_exists_in_config(self):
        channel = Mock()
        channel.exchange_declare = Mock()
        queue_name = ''
        qos = 1
        config = Mock()
        config.has_option = Mock(side_effect=lambda *x: {
            ('rabbitmq', 'prefetch count'): True}[x])
        config.get = Mock(side_effect=lambda *x: {
            ('rabbitmq', 'exchange'): '',
            ('rabbitmq', 'routing keys'): '',
            ('rabbitmq', 'prefetch count'): qos}[x])
        d = dec.TopicsDeclarator()

        d.execute(channel=channel, queue_name=queue_name, config=config)

        channel.basic_qos.assert_called_with(prefetch_count=qos)

    def test_should_not_set_prefetch_count_if_value_doesnt_exist(self):
        channel = Mock()
        channel.exchange_declare = Mock()
        queue_name = ''
        qos = 1
        config = Mock()
        config.has_option = Mock(side_effect=lambda *x: {
            ('rabbitmq', 'prefetch count'): False}[x])
        config.get = Mock(side_effect=lambda *x: {
            ('rabbitmq', 'exchange'): '',
            ('rabbitmq', 'routing keys'): ''}[x])
        d = dec.TopicsDeclarator()

        d.execute(channel=channel, queue_name=queue_name, config=config)

        channel.basic_qos.assert_not_called()
