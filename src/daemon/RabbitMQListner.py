__author__ = 'Luigi'

import pika
import json
from io import StringIO
from Dispatcher import Dispatcher
import sys,traceback

ids=0

def Listner(Host,Port,SSL,QueueName,ExchangeName):

    if SSL:
        connection = pika.BlockingConnection( pika.ConnectionParameters(Host,Port,ssl=True, ssl_options=SSL))
    else:
        connection = pika.BlockingConnection( pika.ConnectionParameters(Host,Port))

    channel = connection.channel()

    disp=Dispatcher()
    disp.loadAlgorithms('Configurations/Algorithms.yml')
    disp.loadCommands('Configurations/Commands.json')

    channel.exchange_declare(exchange=ExchangeName,durable=True)
    channel.queue_declare(queue=QueueName)


    channel.queue_bind(exchange=ExchangeName,queue=QueueName)


    channel.exchange_declare(exchange='rpc_queue')
    channel.queue_declare(queue='rpc_queue')


    channel.queue_bind(exchange='rpc_queue',queue='rpc_queue')

    print (' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):


        text=body.decode(encoding="utf-8", errors="strict")
        print(text)
        if (text=='Hello World!') or (text=='hello'):
            ch.basic_ack(delivery_tag = method.delivery_tag)
            return
        Stringio = StringIO(body)
        data = json.load(Stringio)

        if data['Command'] == disp.getCommand('Add Participant'):
            print ('Add-Participant')
            print(disp.addParticipant(data['Participant']))
            print ('Everything OK')

        if data['Command'] == disp.getCommand('Insert Event'):
            print ('Add-Compute')
            global ids
            data['Event']['ID']= str(ids)
            ids = ids +1

            eve=disp.inserEvent(data['Participant'],data['Event'])
            if not eve:
                print("Somenthing wrong!!")
            else:
                print("EventID:"+ str(eve[0]))
                disp.compute(data['Participant'],eve)

        print (" [x] Done!")
        ch.basic_ack(delivery_tag = method.delivery_tag)


    def on_request(ch, method, props, body):

        #print(body)

        try:

            text=body.decode(encoding="utf-8", errors="strict")

            Stringio = StringIO(text)
            data = json.load(Stringio)

            print(data)

            if data['Command'] == disp.getCommand('Add Participant'):
                print ('Add Participant')
                ret=disp.addParticipant(data['Participant'])
                if ret:
                    response='ACK From Add Participant'
                else:
                    response='NACK From Add Participant'


            if data['Command'] == disp.getCommand('Insert Event'):
                print ('Insert Event')

                global ids
                data['Event']['ID']= str(ids)+'_'+data['TimeStamp']+'_'+data['Participant']
                ids = ids +1

                eve=disp.inserEvent(data['Participant'],data['Event'])
                if not eve:
                    response='NACK From Insert Event'
                else:
                    print("EventID:"+ str(eve[0]))
                    disp.compute(data['Participant'],eve)
                    response='ACK From Insert Event'


            if data['Command'] == disp.getCommand('List Event'):

                response=''

                for event in disp.getAllEventFromParticipant(data['Participant']):
                    #print(event)
                    printevent= event.getPrintEvent()
                    response=response+str(printevent)+'\n'

                if response=='':
                    response='Nothing to show From List Event'

            if data['Command'] == disp.getCommand('Delete Event'):

                ret=disp.deleteEvent(data['Participant'],data['Event'])
                if ret:
                    response='ACK From List Event'
                else:
                    response='NACK From List Event'


            if data['Command'] == disp.getCommand('Delete Password'):
                ret=disp.deletePassword(data['Participant'],data['Password'])
                if ret:
                    response='ACK From Delete Password'
                else:
                    response='NACK Frome Delete Password'

            if data['Command'] == disp.getCommand('Delete WebSite'):
                None

            if data['Command'] == disp.getCommand('Delete All Event'):
                ret=True

                for event in disp.getAllEventFromParticipant(data['Participant']):
                    #print(event)
                    ret=ret and disp.deleteEvent(data['Participant'],event.data['ID'])
                if ret:
                    response='ACK From All Event'
                else:
                    response='NACK From All Event'


            if data['Command'] == disp.getCommand('Delete Participant'):

                ret=disp.deleteParticipant(data['Participant'])
                if ret:
                    response='ACK From Delete Participant'
                else:
                    response='NACK From Delete Participant'

            ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=response)
            ch.basic_ack(delivery_tag = method.delivery_tag)
            print(response)
        except:
            traceback.print_exc(file=sys.stdout)
            ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body='ERROR SOMETHING GOES WRONG!')
            ch.basic_ack(delivery_tag = method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='rpc_queue')
    channel.start_consuming()

def main():

    Host='localhost'
    Port = 5671
    Ssl = ({
    'certfile' : '/Users/Luigi/Sites/Internship/rabbitmq_server-3.5.4/Certificate/client/cert.pem',
    'keyfile': '/Users/Luigi/Sites/Internship/rabbitmq_server-3.5.4/Certificate/client/key.pem',
    'server_side': False})
    Name='hello'

    Listner(Host,Port,Ssl,Name,Name)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt):
        print("BYE!!")
