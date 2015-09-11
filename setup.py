__author__ = 'Luigi'

import sys
import subprocess

listofpackage = ['pika','scrypt','nltk','wordsegment','zxcvbn']

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
            subprocess.call(['pip', 'install', name])
    import nltk
    nltk.download()