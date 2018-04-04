import logging
from rabbitmq.RBMapPoolPublisher import *

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    amqp_url = 'amqp://admintest:admintest123@localhost:5672/?socket_timeout=10&connection_attempts=2'
    routing_key = 'nghiatest'
    for i in range(100):
        message = {u'111': u'aaa',
                   u'222': u'bbb',
                   u'333': u'ccc',
                   u'numMsg': i}

        pool = RBMapPoolPublisher().get_pool_publisher(amqp_url, routing_key)
        pool.send_msg(message)
        logger.info('Published message # %i', i)
