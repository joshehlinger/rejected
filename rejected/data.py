"""
Rejected data objects

"""
import copy


class Data(object):

    __slots__ = []

    def __iter__(self):
        """Iterate the attributes and values as key, value pairs.

        :rtype: tuple

        """
        for attribute in self.__slots__:
            yield (attribute, getattr(self, attribute))

    def __repr__(self):
        """Return a string representation of the object and all of its
        attributes.

        :rtype: str

        """
        items = ['%s=%s' % (k, getattr(self, k))
                 for k in self.__slots__ if getattr(self, k)]
        return '<%s(%s)>' % (self.__class__.__name__, items)


class Message(Data):
    """Class for containing all the attributes about a message object creating a
    flatter, move convenient way to access the data while supporting the legacy
    methods that were previously in place in rejected < 2.0

    """
    __slots__ = ['channel', 'method', 'properties', 'body', 'consumer_tag',
                 'delivery_tag', 'exchange', 'redelivered', 'routing_key']

    def __init__(self, channel, method, header, body):
        """Initialize a message setting the attributes from the given channel,
        method, header and body.

        :param channel: The channel the message was received on
        :type channel: pika.channel.Channel
        :param pika.frames.Method method: pika Method Frame object
        :param pika.frames.Header header: pika Header Frame object
        :param str body: Opaque message body

        """
        self.channel = channel
        self.method = method
        self.properties = Properties(header.properties)
        self.body = copy.copy(body)

        # Map method properties
        self.consumer_tag = method.consumer_tag
        self.delivery_tag = method.delivery_tag
        self.exchange = method.exchange
        self.redelivered = method.redelivered
        self.routing_key = method.routing_key


class Properties(Data):
    """A class that represents all of the field attributes of AMQP's
    Basic.Properties

    """
    __slots__ = ['app_id', 'cluster_id', 'content_type', 'content_encoding',
                 'correlation_id', 'delivery_mode', 'expiration', 'headers',
                 'priority', 'reply_to', 'message_id', 'timestamp', 'type',
                 'user_id']

    def __init__(self, properties=None):
        """Create a base object to contain all of the properties we need

        :param pika.spec.BasicProperties properties: pika.spec.BasicProperties

        """
        if properties:
            self.app_id = properties.app_id
            self.cluster_id = properties.cluster_id
            self.content_type = properties.content_type
            self.content_encoding = properties.content_encoding
            self.correlation_id = properties.correlation_id
            self.delivery_mode = properties.delivery_mode
            self.expiration = properties.expiration
            self.headers = properties.headers
            self.priority = properties.priority
            self.reply_to = properties.reply_to
            self.message_id = properties.message_id
            self.timestamp = properties.timestamp
            self.type = properties.type
            self.user_id = properties.user_id
        else:
            for attr in self.__slots__:
                setattr(self, attr, None)
