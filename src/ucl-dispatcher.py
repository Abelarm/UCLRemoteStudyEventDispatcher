__author__ = 'Luigi'

import os,sys
import ConfPath as cf
import argparse

parser = argparse.ArgumentParser(description='UCL Dispatcher')
parser.add_argument('address',metavar='Host [localhost]',type=str,help='address of RabbitMQ server')
parser.add_argument('port',metavar='Port [5672]',type=str,help='port of RabbitMQ server')
parser.add_argument('name',metavar='ExchangeName [hello]',type=str,help='name of exchange queue')
parser.add_argument('--path',metavar='PATH',help='path where key and cert are located')
args = parser.parse_args()


cwd = os.path.dirname(os.path.abspath(__file__))
with open(cwd+'/.prefixpath','r') as f:
        cf.paths['prefix'] =f.read()
sys.path.insert(1, cf.paths['prefix']+cf.paths['main'])

from RabbitMQListner import Listner
if args.path:
    path= args.path
    if path.endswith('/'):
        path = path[:-1]
    Ssl = ({
        'certfile' : path+'/cert.pem',
        'keyfile': path+'/key.pem',
        'server_side': False})
else:
    Ssl = None

Listner(args.address,args.port,Ssl,cf.paths)

print(cf.paths['main'])