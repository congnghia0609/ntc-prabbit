import logging
from rabbitmq.RBConsumerImp import *
from rabbitmq.RBTConsumerImp import *
from rabbitmq.RBConsumeManager import *

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    manager = RBConsumeManager()

    routing_key = 'nghiatest'
    rbconsumer1 = RBConsumerImp('amqp://admintest:admintest123@localhost:5672/%2F', routing_key=routing_key)
    rbconsumer2 = RBConsumerImp('amqp://admintest:admintest123@localhost:5672/%2F', routing_key=routing_key)
    rbconsumer3 = RBConsumerImp('amqp://admintest:admintest123@localhost:5672/%2F', routing_key=routing_key)
    rbtconsumer = RBTConsumerImp('amqp://admintest:admintest123@localhost:5672/%2F', routing_key=routing_key)

    manager.add(rbconsumer1)
    manager.add(rbconsumer2)
    manager.add(rbconsumer3)
    manager.add(rbtconsumer)

    try:
        manager.start()
    except Exception as e:
        logging.error("test_consume_manager run fail...")


if __name__ == '__main__':
    main()
