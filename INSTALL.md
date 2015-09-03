For installing this dispatcher, first you need to install RabbitMQ.
use this link https://www.rabbitmq.com/download.html

If you want to enable SSL communications in /data you can find
an example of configuration file for rabbitMQ
reference: https://www.rabbitmq.com/ssl.html

ensure that RabbitMQ works.

Run setup.py
     -c install #For installing in /home/daemon
     -p path #For installing in different path

Python 3.3+, pip is needed