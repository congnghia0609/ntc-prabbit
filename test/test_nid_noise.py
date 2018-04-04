import logging
from rabbitmq.NIdNoise import *

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    for i in range(100):
        id1 = i
        nid1 = NIdNoise.get_instance().ennoise_id(id=id1)
        logging.info("id1: " + str(id1) + " --> nid1: " + str(nid1))

        nid2 = nid1
        id2 = NIdNoise.get_instance().denoise_id(nid=nid2)
        logging.info("nid2: " + str(nid2) + " --> id2: " + str(id2))
        logging.info("id1 == id2: %s", str(id1 == id2))
