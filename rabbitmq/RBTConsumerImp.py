import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from rabbitmq.RBAsynTConsumer import *


LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


class RBTConsumerImp(RBAsynTConsumer):

    def process_message(self, basic_deliver, properties, body):
        """Child Class extends Class RBAsynTConsumer and Override this method processMessage"""
        logger.info('============ RBTConsumerImp process message ============')
        # do something...

    def start_consumer(self):
        ct = self.ConsumerThread(self)
        ct.start()

    class ConsumerThread (threading.Thread):
        def __init__(self, consumer=None):
            threading.Thread.__init__(self)
            self.consumer = consumer

        def run(self):
            try:
                logging.info("Instance ConsumerThread[%s] starting...", self.consumer.ROUTING_KEY)
                self.consumer.run()
            except Exception as e:
                logging.info("Instance ConsumerThread[%s] run fail...", self.consumer.ROUTING_KEY)
                self.consumer.stop()
