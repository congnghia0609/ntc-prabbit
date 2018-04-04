import logging
from rabbitmq.RBPoolPublisher import *

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


class RBMapPoolPublisher:

    map_pool_publisher = {}

    def get_pool_publisher(self, amqp_url, routing_key):
        if self.map_pool_publisher.get(routing_key):
            logging.info("***** Re-Use RBPoolPublisher[%s]... *****", routing_key)
            return self.map_pool_publisher.get(routing_key)
        else:
            logging.info("$$$$$ Create new RBPoolPublisher[%s]... $$$$$", routing_key)
            pool = RBPoolPublisher(amqp_url=amqp_url, routing_key=routing_key)
            self.map_pool_publisher[routing_key] = pool
            return pool
