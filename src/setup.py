__author__ = 'Luigi'

import sys,os,argparse
import subprocess
import glob,shutil
import ConfPath as cf
from pprint import pprint


parser = argparse.ArgumentParser(description='UCL Dispatcher installer')
parser.add_argument('command',metavar='install uninstall',type=str,help='command')
parser.add_argument('-path',metavar='Path [/path/path]',type=str,help='root path where Dispatcher will be installed')

args = parser.parse_args()
if args.command=='install':

    cwd=os.path.dirname(os.path.abspath(__file__))
    if cwd.endswith('/'):
            cwd = cwd[:-1]

    if args.path:
        prefix = args.path
    else:
        prefix = os.path.abspath(os.path.join(cwd, os.pardir))

    if prefix.endswith('/'):
            prefix = prefix[:-1]

    with open(cwd+'/.prefixpath','w+') as f:
        f.write(prefix)


    listofpackage = ['pika','scrypt','nltk','wordsegment','zxcvbn','os']

    req_version = (3,3)
    cur_version = sys.version_info

    if cur_version < req_version:
        print ("Your Python interpreter is too old. Please consider upgrading.")
        sys.exit(1)

    try:
        import setuptools
    except ImportError:
        print ('Install pip')
        sys.exit(1)
    else:
        installed_package=sys.modules.keys()
        for name in listofpackage:
            if name not in installed_package:
                print('Installing: ' +name)
                subprocess.call(['pip', 'install', name])
        import nltk
        print('Downloading: nltk corpus')
        nltk.download()



    sourcepath = cwd+'/daemon'
    algsourcepath = cwd+'/daemon/algorithms/'

    sorucefile = glob.glob(sourcepath+'/*.py')

    for key in cf.paths:
        if key=='projectname':
            continue
        print('Creating: '+prefix+cf.paths[key])
        os.makedirs(prefix+cf.path[key])

        if key=='ConfigAlgorithms':
            print('Creating: '+prefix+cf.paths[key]+'AlgorithmsDB')
            open(str(prefix+cf.paths[key])+'/AlgorithmsDB','w+')
        if key=='ConfigAlgorithms':
            print('Creating: '+prefix+cf.paths[key]+'CommandsDB')
            open(str(prefix+cf.paths[key])+'/CommandsDB','w+')


    for f in sorucefile:
        print('copying: '+f +' => '+prefix+cf.paths['main'])
        shutil.copy(f,prefix+cf.paths['main'])

    print('copying: '+cwd+'/Confpath.py' +' => '+prefix)
    shutil.copy(cwd+'/Confpath.py',prefix)
    print('copying: '+cwd+'/ucl-dispatcher.py' +' => '+prefix)
    shutil.copy(cwd+'/ucl-dispatcher.py',prefix)


    for x in os.listdir(algsourcepath):
        if not x.startswith('.'):
            print('copying: '+algsourcepath+x +' => '+prefix+cf.paths['Algorithms'])
            shutil.copytree(x,prefix+cf.paths['Algorithms'])

elif args.command=='uninstall':

    cwd=os.path.dirname(os.path.abspath(__file__))
    if cwd.endswith('/'):
            cwd = cwd[:-1]


    with open(cwd+'/.prefixpath','r') as f:
        prefix =f.read()


    for key in cf.paths:
        if key=='projectname':
            continue
        print('Removing: '+prefix+cf.paths[key])
        shutil.rmtree(x,prefix+cf.paths[key])





