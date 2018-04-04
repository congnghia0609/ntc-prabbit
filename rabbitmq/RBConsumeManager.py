import logging
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import threading

logger = logging.getLogger(__name__)


class RBConsumeManager:

    def __init__(self):
        self.listConsumer = []

    def add(self, consumer):
        self.listConsumer.append(consumer)

    def start(self):
        if len(self.listConsumer):
            for c in self.listConsumer:
                try:
                    c.start_consumer()
                except Exception as e:
                    logger.error("Consumer[%s] start fail...", c.ROUTING_KEY)
            logger.info("=====>>> RBConsumeManager start successfully...")
        else:
            logger.info("RBConsumeManager is empty...")
