import logging
from rabbitmq.RBPoolPublisher import *
from rabbitmq.RBMapPoolPublisher import *
from concurrent.futures import *
import threading
from threading import Thread

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


def run_task(begin=0):
    routing_key = 'nghiatest'
    amqp_url = 'amqp://admintest:admintest123@localhost:5672/?socket_timeout=10&connection_attempts=2'

    for i in range(begin, begin + 100, 1):
        message = {u'111': u'aaa',
                   u'222': u'bbb',
                   u'333': u'ccc',
                   u'numMsg': i}

        pool = RBMapPoolPublisher().get_pool_publisher(amqp_url, routing_key)
        pool.send_msg(message)
        logger.info('Published message # %i', i)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     future1 = executor.submit(runTask(0))
    #     logging.info("---->>> future1: %s", future1)
    #     future2 = executor.submit(runTask(300))
    #     logging.info("---->>> future2: %s", future2)
    #     future3 = executor.submit(runTask(600))
    #     logging.info("---->>> future3: %s", future3)

    thread1 = Thread(target=run_task(0))
    thread2 = Thread(target=run_task(300))
    thread3 = Thread(target=run_task(600))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
