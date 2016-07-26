#!/usr/bin/env python

import boto3, os.path, inspect, time, pika, ConfigParser, overrides as ov, sys

config = None
kinesis_write_delay = 0


class RabbitMqChannelFactory(object):

    @staticmethod
    def create_channel(url):
        connection = pika.BlockingConnection(pika.URLParameters(url=url))
        return connection.channel()


def start_consume(channel,
                  channel_declarator,
                  loc_config,
                  queue_name,
                  no_ack=True,):

    channel.queue_declare(queue=queue_name)

    if channel_declarator:
        channel_declarator.execute(channel, queue_name, loc_config)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=no_ack)

    channel.start_consuming()


def callback(ch, method, properties, body):
    k = boto3.client('kinesis')
    time.sleep(kinesis_write_delay)
    partition_key = ov.get_stream_partition_key(method)
    k.put_record(StreamName=config.get('kinesis', 'stream'),
                 Data=body,
                 PartitionKey=partition_key)


def get_config(filename):
    conf = ConfigParser.ConfigParser()
    conf.read(filename)
    return conf


def main():
    args = sys.argv[1:]
    global config, kinesis_write_delay
    config = get_config(args[0])
    kinesis_write_delay = int(config.get('kinesis', 'write delay'))
    channel = RabbitMqChannelFactory.create_channel(url=config.get('rabbitmq',
                                                                   'url'))
    declarator = ov.get_declarator()
    queue_name = config.get('rabbitmq', 'queue')

    start_consume(channel=channel, channel_declarator=declarator,
                  loc_config=config, queue_name=queue_name)


if __name__ == '__main__':
    main()
