#!/usr/bin/env python
# -*- coding: utf8
'''
Determines the maximum number of characters in a field of the 
TCU file
'''

__author__ = 'Flavio Figueiredo (flaviov at gmail dot com)'

import sys

if __name__ == '__main__':
    to_sort = []
    
    with open(sys.argv[1]) as tcu_file:
        for line in tcu_file:
            spl = line.split(',')
            to_sort.extend(len(field) for field in spl)
    
    to_sort.sort()
    print to_sort[-1]
