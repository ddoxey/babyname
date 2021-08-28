#!/usr/bin/env python3

import sys
from pprint import pprint
from babyname import BabyName


def run(name, start=1900, gender=None):

    bn = BabyName()
    x = bn.lookup(name, start, gender)
    pprint(x)


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print('USAGE: {sys.argv[0]} <name> [<start-year>] [<gender>]', file=sys.stderr)
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    elif len(sys.argv) == 3:
        run(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        run(sys.argv[1], sys.argv[2], sys.argv[3])
