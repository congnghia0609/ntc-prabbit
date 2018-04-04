import json
import logging
import pika
import pika_pool

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


class RBPoolPublisher:
    # # Here will be the instance stored.
    # __instance = None
    #
    # @staticmethod
    # def getInstance(amqp_url, routing_key):
    #     """ Static access method. """
    #     if RBPoolPublisher.__instance == None:
    #         RBPoolPublisher(amqp_url, routing_key)
    #     return RBPoolPublisher.__instance
    #
    # def __init__(self, amqp_url, routing_key):
    #     """ Virtually private constructor. """
    #     if RBPoolPublisher.__instance != None:
    #         raise Exception("RBPoolPublisher class is a singleton!")
    #     else:
    #         if (amqp_url and routing_key) :
    #             self.amqp_url = amqp_url
    #             self.routing_key = routing_key
    #             self.params = pika.URLParameters(amqp_url)
    #             self.pool = pika_pool.QueuedPool(
    #                     # create=lambda: pika.BlockingConnection(parameters=params),
    #                     create=lambda: self.createConnection(),
    #                     max_size=100,
    #                     max_overflow=10,
    #                     timeout=10,
    #                     recycle=3600,
    #                     stale=45,
    #                 )
    #
    #             RBPoolPublisher.__instance = self
    #         else:
    #             raise Exception("amqp_url or routing_key much not empty!")

    def __init__(self, amqp_url, routing_key):
        if amqp_url and routing_key:
            self.amqp_url = amqp_url
            self.routing_key = routing_key
            self.params = pika.URLParameters(amqp_url)
            self.pool = pika_pool.QueuedPool(
                    # create=lambda: pika.BlockingConnection(parameters=params),
                    create=lambda: self.create_connection(),
                    max_size=100,
                    max_overflow=10,
                    timeout=10,
                    recycle=3600,
                    stale=45,
                )
        else:
            raise Exception("amqp_url or routing_key much not empty!")

    def create_connection(self):
        # Open a connection to RabbitMQ on localhost using all default parameters
        connection = pika.BlockingConnection(parameters=self.params)
        # Open the channel
        channel = connection.channel()
        # Declare the queue
        # queue="text" : Queue name.
        # durable=True : Msg persistent to file. Msg not loss when RabbitMQ quits or crashes or restart.
        # exclusive=False : disconnect the consumer the queue should not be deleted. True: queue should be deleted.
        # auto_delete=False : Not remove when no more queues are bound to it.
        channel.queue_declare(queue=self.routing_key, durable=True, exclusive=False, auto_delete=False)
        # Turn on delivery confirmations
        channel.confirm_delivery()

        return connection

    def send_msg(self, message=None):
        if message:
            cxn = self.pool.acquire()
            try:
                properties = pika.BasicProperties(content_type='application/json',
                                                  content_encoding='utf-8',
                                                  # headers=message,
                                                  delivery_mode=2,  # make message persistent
                                                  app_id='rbSinglePoolPublisher_' + self.routing_key
                                                  )
                cxn.channel.basic_publish(
                    exchange=self.routing_key,
                    routing_key=self.routing_key,
                    body=json.dumps(message, ensure_ascii=False),
                    properties=properties
                )
            except Exception as e:
                logger.error("Error RBPoolPublisher.sendMsg: ", e)
            finally:
                cxn.release()
        else:
            logger.info('message[%s] is empty!!!...', routing_key, message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    # message_number = 0

    amqp_url = 'amqp://admintest:admintest123@localhost:5672/?socket_timeout=10&connection_attempts=2'
    routing_key = 'nghiatest'
    for i in range(100):
        message = {u'111': u'aaa',
                   u'222': u'bbb',
                   u'333': u'ccc',
                   u'numMsg': i}

        pool = RBPoolPublisher(amqp_url, routing_key)
        pool.send_msg(message)
        logger.info('Published message # %i', i)
        # message_number = message_number + 1
