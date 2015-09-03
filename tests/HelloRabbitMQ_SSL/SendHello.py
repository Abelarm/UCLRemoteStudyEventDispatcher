import pika


ssl_options = ({'certfile': '/path/to/your/cacert.pem',
  'certfile' : '/path/to/your/client/cert.pem',
  'keyfile': '/path/to/your/client/key.pem',
  'server_side': False})

connection = pika.BlockingConnection( pika.ConnectionParameters('localhost', 5671,ssl=True, ssl_options=ssl_options))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()