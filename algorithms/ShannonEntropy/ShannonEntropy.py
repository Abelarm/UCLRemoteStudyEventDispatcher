__author__ = 'Luigi'

import math
from collections import Counter

def entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum( count/lns * math.log(count/lns, 2) for count in p.values())


if __name__ == '__main__':

    print(entropy('Tr0ub4dour&3'))