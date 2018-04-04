import logging
from rabbitmq.RBConsumerImp import *
from rabbitmq.RBTConsumerImp import *

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    routing_key = 'nghiatest'
    rbconsumer = RBConsumerImp('amqp://admintest:admintest123@localhost:5672/%2F', routing_key)
    try:
        rbconsumer.run()
    except KeyboardInterrupt:
        rbconsumer.stop()


if __name__ == '__main__':
    main()
