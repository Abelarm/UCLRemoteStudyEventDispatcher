__author__ = 'Luigi'

import Zxcvbn as zx
import pprint

def Zxcvbn(Password,path=None):

    if path:
        file = path+'zxcvbn'
    else:
        file = 'zxcvbn'

    with open (file,'w+') as f:

        f.write('OMINIMATCH:\n\n')
        f.write(pprint.pformat(zx.main.omnimatch(Password)))
        f.write('\n\nPASSWORD STRENGTH:\n\n')
        f.write(pprint.pformat(zx.main.password_strength(Password)))