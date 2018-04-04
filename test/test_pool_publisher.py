import logging
import time
from rabbitmq.RBPoolPublisher import *

current_milli_time = lambda: int(round(time.time() * 1000))

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    # # make_thumb | uploads3 | img_to_pdf
    # routing_key = 'img_to_pdf'
    # amqp_url = 'amqp://admintest:admintest123@localhost:5672/?socket_timeout=10&connection_attempts=2'
    #
    # message = {'pathFile': u'/data/files/tmp/cat.jpg', 'id': 30}
    # # message = {'pathFile': u'/data/files/tmp/30.png', 'id': 30}
    # # message = {'pathFile': u'/data/files/tmp/BI0.doc', 'id': 30}
    # # message = {'pathFile': u'/data/files/tmp/BI.odt', 'id': 30}
    #
    # # message = {'pathFile': u'/data/files/tmp/12.jpg', 'fid': 12, 'uid': 1, 'rid': 2, 'isShare': True}
    # # metadata = {}
    # # metadata['content_type'] = "image/jpg"
    # # metadata['title'] = "12.jpg"
    # # metadata['description'] = "description 12.jpg"
    # # metadata['owner'] = "nghia"
    # # metadata['modified_date'] = current_milli_time()
    # # metadata['modified_by'] = "nghia"
    # # metadata['opened_date'] = current_milli_time()
    # # metadata['created_date'] = current_milli_time()
    # # message['metadata'] = metadata
    #
    # print('message: ' + str(message))
    # pool = RBPoolPublisher(amqp_url, routing_key)
    # pool.send_msg(message)
    # logger.info('Published message # %s', str(message))

    routing_key = 'nghiatest'
    amqp_url = 'amqp://admintest:admintest123@localhost:5672/?socket_timeout=10&connection_attempts=2'
    for i in range(100):
        message = {u'111': u'aaa',
                   u'222': u'bbb',
                   u'333': u'ccc',
                   u'numMsg': i}

        pool = RBPoolPublisher(amqp_url, routing_key)
        pool.sendMsg(message)
        logger.info('Published message # %i', i)
