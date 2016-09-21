#!/usr/bin/env python

import boto3, time, pika, ConfigParser, declarator, \
    partitioner, sys, re, inspect

config = None
kinesis_write_delay = 0
k = None
partitioner_override = None


class RabbitMqChannelFactory(object):

    @staticmethod
    def create_channel(url):
        connection = pika.BlockingConnection(pika.URLParameters(url=url))
        return connection.channel()


def load_override(module, regex=None):
    cls = None
    if regex:
        try:
            overs = [(name, value) for (name, value) in inspect.getmembers(
                module, inspect.isclass) if re.search(regex, name)]
            if len(overs) > 1:
                raise ValueError('Too many overrides of the same type found in '
                                 'module')
            (name, value) = overs[0]
            cls = getattr(module, name)()
        except AttributeError as e:
            print(e)
            raise

    return cls


def load_declarator():
    return load_override(declarator, regex='Declarator$')


def load_partitioner():
    return load_override(partitioner, regex='Partitioner$')


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

    print ('Start consuming...')
    channel.start_consuming()


def callback(ch, method, properties, body):
    if kinesis_write_delay > 0:
        time.sleep(kinesis_write_delay)
    partition_key = partitioner_override.get_stream_partition_key(method)
    k.put_record(StreamName=config.get('kinesis', 'stream'),
                 Data=body,
                 PartitionKey=partition_key)
    print('Record {0} published'.format(method.delivery_tag))


def get_config(filename):
    conf = ConfigParser.ConfigParser()
    conf.read(filename)
    return conf


def main():
    args = sys.argv[1:]
    global config, kinesis_write_delay, k, partitioner_override
    config = get_config(args[0])
    kinesis_write_delay = int(config.get('kinesis', 'write delay'))
    k = boto3.client('kinesis', region=config.get('kinesis', 'region'))
    channel = RabbitMqChannelFactory.create_channel(url=config.get('rabbitmq',
                                                                   'url'))
    declarator_override = load_declarator() if len(args) > 1 else None
    partitioner_override = load_partitioner()
    queue_name = config.get('rabbitmq', 'queue')

    start_consume(channel=channel, channel_declarator=declarator_override,
                  loc_config=config, queue_name=queue_name)


if __name__ == '__main__':
    main()
