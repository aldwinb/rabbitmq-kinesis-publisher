class RabbitMqDeclarator(object):
    def execute(self, channel, queue_name, config):
        pass


class TopicsDeclarator(RabbitMqDeclarator):
    def execute(self, channel, queue_name, config):
        exchange = config.get('rabbitmq', 'exchange')
        channel.exchange_declare(exchange=exchange,
                                 type='topic')
        routing_keys = config.get('rabbitmq', 'routing keys').split(',')
        for routing_key in routing_keys:
            channel.queue_bind(exchange=exchange,
                               queue=queue_name,
                               routing_key=routing_key)
        if config.has_option('rabbitmq', 'prefetch count'):
            channel.basic_qos(prefetch_count=int(config.get('rabbitmq',
                                                            'prefetch count')))
