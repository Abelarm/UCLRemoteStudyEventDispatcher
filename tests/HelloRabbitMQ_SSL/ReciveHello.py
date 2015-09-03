import pika


ssl_options = ({'certfile': '/path/to/your/cacert.pem',
  'certfile' : '/path/to/your/client/cert.pem',
  'keyfile': '/path/to/your/client/key.pem',
  'server_side': False})

connection = pika.BlockingConnection( pika.ConnectionParameters('localhost', 5671,ssl=True, ssl_options=ssl_options))
channel = connection.channel()

channel.queue_declare(queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print (" [x] Received %r" % (body,))

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

channel.start_consuming()
