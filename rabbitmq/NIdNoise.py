import logging
from hashids import Hashids

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


class NIdNoise:
    NSALT = "dakjsl#^%6bqhcjhb"
    HASH_LENGTH = 11

    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if NIdNoise.__instance == None:
            NIdNoise()
        return NIdNoise.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if NIdNoise.__instance != None:
            raise Exception("NIdNoise class is a singleton!")
        else:
            self.hashids = Hashids(salt=self.NSALT, min_length=self.HASH_LENGTH)
            NIdNoise.__instance = self

    def ennoise_id(self, id):
        if id >= 0:
            return self.hashids.encode(id)
        else:
            return ''

    def denoise_id(self, nid):
        if nid:
            return self.hashids.decode(nid)[0]
        else:
            return ''


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
