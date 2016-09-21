# rabbitmq-kinesis-publisher #

A simple program that forwards messages from RabbitMQ queue to an AWS Kinesis stream.
It runs on Docker.

### Usage ###

At the minimum, you need the following:

##### AWS credentials #####
You need at least the credentials and config files, 
stored together in a directory. For more information, please see [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

##### Configuration file ###### 
This should be in .ini format and named config.ini. The required values are:
* RabbitMQ section
  * url - The address of the RabbitMQ cluster. It should follow the 
  [AMQP scheme](https://www.rabbitmq.com/uri-spec.html) (e.g. 
  amqp://user:pass@host:10000/vhost)
  * queue - The name of the queue that you will consume messages from
* Kinesis section  
  * stream - The name of the stream to publish messages to
  * region - The AWS region of the Kinesis stream
  * write delay - The time (in seconds) that the app will wait before 
  sending another message into the stream. This is to prevent from hitting 
  the [AWS Kinesis stream limits](http://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html). 
  A value of zero (0) means no wait time.

A sample of the config file can be seen in the samples directory.

##### Command to run the app #####
```shell
docker run \
-v <dir_of_AWS_credentials_files:/root/.aws \
-v <dir_of_config_file>:/usr/src/app/config \
-d \
aldwinb/rabbitmq-kinesis-publisher
```

### Declarators and partitioners ###

To follow

### Support for AWS STS tokens ###

To follow