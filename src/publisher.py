#!/usr/bin/env python

import boto3, os.path, inspect, time, pika, ConfigParser
import overrides as ov

config = None


def start_consume():

    queue_name = config.get('rabbitmq', 'queue')
    connection = pika.BlockingConnection(pika.URLParameters(
        url=config.get('rabbitmq', 'url')))

    channel = connection.channel()
    channel.queue_declare(queue_name=queue_name)

    declarator = ov.get_declarator()
    declarator.execute(channel, queue_name, config)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()


def callback(ch, method, properties, body):
    k = boto3.client('kinesis')
    time.sleep(0.005)
    partition_key=ov.get_stream_partition_key()
    k.put_record(StreamName=config.get('kinesis', 'stream'),
                 Data=body,
                 PartitionKey=partition_key)


def get_config(filename):
    conf = ConfigParser.ConfigParser()
    conf.read(filename)
    return conf


def main():
    pre_path = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    global config
    config = get_config(os.path.join(pre_path, 'config.ini'))


if __name__ == '__main__':
    main()