import logging
from .RBMapPoolPublisher import *

logger = logging.getLogger(__name__)


def send_msg(routing_key, message):
    if routing_key and message:
        amqp_url = 'amqp://admintest:admintest123@localhost:5672/?socket_timeout=10&connection_attempts=2'
        pool = RBMapPoolPublisher().get_pool_publisher(amqp_url=amqp_url, routing_key=routing_key)
        pool.send_msg(message)
        logger.info('Published message [Key=%s | Value=%s] successfully...', routing_key, message)
    else:
        logger.info('[Key=%s | Value=%s] much not empty...', routing_key, message)
