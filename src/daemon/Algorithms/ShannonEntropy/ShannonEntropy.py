__author__ = 'Luigi'

import math
from collections import Counter

def ShannonEntropy(s,path=None):
    if path:
        filename=path+'ShannonEntropy'
    else:
        filename= 'ShannonEntropy'
    p, lns = Counter(s), float(len(s))
    with open (filename,'w+') as f:
        f.write(str(-sum( count/lns * math.log(count/lns, 2) for count in p.values())))


#if __name__ == '__main__':

    #print(ShannonEntropy('Tr0ub4dour&3'))