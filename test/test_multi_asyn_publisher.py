import logging
from rabbitmq.RBPoolPublisher import *
from rabbitmq.RBAsynPublisher import *
from concurrent.futures import *
import threading
from threading import Thread

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


def run_task():
    routing_key = 'nghiatest'
    rbpublisher = RBAsynPublisher(
        'amqp://admintest:admintest123@localhost:5672/%2F?connection_attempts=3&heartbeat_interval=3600',
        routing_key=routing_key, interval=0.2)
    try:
        rbpublisher.run()
    except KeyboardInterrupt:
        rbpublisher.stop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    # with ProcessPoolExecutor(max_workers=3) as executor:
    #     future1 = executor.submit(runTask())
    #     logging.info("---->>> future1: %s", future1)
    #     future2 = executor.submit(runTask())
    #     logging.info("---->>> future2: %s", future2)
    #     future3 = executor.submit(runTask())
    #     logging.info("---->>> future3: %s", future3)

    thread1 = Thread(target=run_task())
    thread2 = Thread(target=run_task())
    thread3 = Thread(target=run_task())

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
