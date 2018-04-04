# ntc-prabbit

**ntc-prabbit** is code template for module RabbitMQ Client: Producer and Consumer.    

### 1. Setup Python 3.4.3

```
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar xzf Python-3.4.3.tgz

cd Python-3.4.3
./configure
sudo make altinstall

# check
python3 -V
```

### 2. Setup virtual environment

  - Linux:  

Install virtualenvwrapper  

```
sudo apt-get install python3-pip
sudo pip3 install virtualenvwrapper
mkdir ~/.virtualenvs
```

Add the following lines to ```~/.bashrc```:  
```
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'
source /usr/local/bin/virtualenvwrapper.sh
```

```
# Create virtualenv
mkvirtualenv ntc-prabbit

# Activate/switch to a virtualenv
workon ntc-prabbit

# Deactivate virtualenv
deactivate ntc-prabbit
```

Install python packages for cooler project which is defined in **requirements.txt**    
Then using this command:  
  - For Windows: <code>pip3.4 install -r requirements.txt</code> (pip3.4 in folder C:\Python34\Scripts)
  - Note: if you can't install with requirements.txt, you can use <code>pip install -r requirements_for_window_os.txt</code>
  - Mac, Linux: <code>pip3 install -r requirements.txt</code>


### 3. Install RabbitMQ

#### 3.1. Ubuntu

Links: [https://www.rabbitmq.com/install-debian.html](https://www.rabbitmq.com/install-debian.html)

##### 3.1.1. Setup RabbitMQ Server
```
sudo apt-get update
sudo apt-get install -y erlang

echo "deb http://www.rabbitmq.com/debian/ testing main" | sudo tee /etc/apt/sources.list.d/rabbitmq.list
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

sudo apt-get update
sudo apt-get install rabbitmq-server
```

##### 3.1.2. Setup Tool Management RabbitMQ

```
sudo rabbitmq-plugins enable rabbitmq_management
```

You can create a new administrator with  

```
sudo rabbitmqctl add_user admintest admintest123
sudo rabbitmqctl set_user_tags admintest administrator
sudo rabbitmqctl set_permissions -p / admintest ".*" ".*" ".*"
```

Chang password account guest  

```
sudo rabbitmqctl change_password guest guest123
```

Delete account guest  

```
sudo rabbitmqctl delete_user guest
```

##### 3.1.3. Run RabbitMQ Server

```
## To start the service:
sudo service rabbitmq-server start

## To stop the service:
sudo service rabbitmq-server stop

## To restart the service:
sudo service rabbitmq-server restart

## To check the status:
sudo service rabbitmq-server status
```

##### 3.1.4. Check RabbitMQ Management on browser

[http://127.0.0.1:15672/](http://127.0.0.1:15672/)

```
Username: admintest
Password: admintest123
```


### 4. Usage RabbitMQ Producer
 
Has 2 ways usage RabbitMQ Producer: **RBSinglePoolPublisher** and **RBMapPoolPublisher**  
  
#### 4.1. Code Template RBSinglePoolPublisher.  
 
RBSinglePoolPublisher is Class Singleton Design Pattern contain pool Publisher.  
  
``` python
import logging
import time
from rabbitmq.RBPoolPublisher import *

current_milli_time = lambda: int(round(time.time() * 1000))

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

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
```
  
#### 4.2. Code Template RBMapPoolPublisher.
  
RBMapPoolPublisher is Class contain dictionary of RBSinglePoolPublisher.  
RBMapPoolPublisher management map RBSinglePoolPublisher  
With Key=routing_key, Value=RBSinglePoolPublisher  
  
``` python
import logging
from rabbitmq.RBMapPoolPublisher import *

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    routing_key = 'nghiatest'
    amqp_url = 'amqp://admintest:admintest123@localhost:5672/?socket_timeout=10&connection_attempts=2'

    for i in range(100):
        message = {u'111': u'aaa',
                   u'222': u'bbb',
                   u'333': u'ccc',
                   u'numMsg': i}

        pool = RBMapPoolPublisher().get_pool_publisher(amqp_url, routing_key)
        pool.send_msg(message)
        logger.info('Published message # %i', i)
```

  
### 5. Usage RabbitMQ RBConsumerImp and RBConsumeManager

RBConsumerImp is template code Consumer.  
You write code in method "processMessage" to process information in "body" datatype json.

``` python
import logging
import threading
from rabbitmq.RBAsynConsumer import *

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)


class RBConsumerImp(RBAsynConsumer):

    def process_message(self, basic_deliver, properties, body):
        """Child Class extends Class RBAsynConsumer and Override this method processMessage"""
        logger.info('============ RBConsumerImp process message ============')
        # do something...
        logging.info("body: " + str(body))

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
```

RBConsumeManager is Class run multi RBConsumerImp.
  
``` python
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
```

## Last Edition  
Editor: nghiatc  
Create: 19/04/2017  
Update: 19/04/2017  

