import logging
from rabbitmq.RBAsynPublisher import *

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    # Connect to localhost:5672 as guest with the password guest and virtual host "/" (%2F)
    # rbpublisher = RBAsynPublisher('amqp://admintest:admintest123@localhost:5672/%2F?connection_attempts=3&heartbeat_interval=3600')
    routing_key = 'nghiatest'
    rbpublisher = RBAsynPublisher(
        'amqp://admintest:admintest123@localhost:5672/%2F?connection_attempts=3&heartbeat_interval=3600',
        routing_key='nghiatest', interval=0.2)
    try:
        rbpublisher.run()
    except KeyboardInterrupt:
        rbpublisher.stop()
