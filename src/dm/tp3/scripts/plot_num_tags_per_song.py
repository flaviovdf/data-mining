# -*- coding: utf8
'''
This scripts plots the CCDF of the number of songs each tag
was assigned to.
'''
from __future__ import division, print_function

from collections import Counter
from matplotlib import pyplot as plt
from scipy import stats
from dm.tp3.lastfm_io import vectorize_songs
from vod.stats.curves import ecdf

import argparse
import sys
import traceback

def main(fpath):
    doc_mat = vectorize_songs(fpath)[0]
    rows = doc_mat.nonzero()[0]
    
    to_plot = Counter(rows).values()
    x, cdf_y = ecdf(to_plot)
    ccdf_y = 1 - cdf_y
    
    print(stats.scoreatpercentile(to_plot, 0.1))
    print(doc_mat.shape)
    ax = plt.gca()
    ax.set_yscale('log')
    ax.set_xscale('log')

    plt.plot(x, ccdf_y, 'bo')
    plt.xlabel('Number Tags per Song (x)')
    plt.ylabel('Prob(Num. Tags per Song > x)')
    plt.title('CCDF of Tags per Song')
    plt.show()

def create_parser(prog_name):
    parser = argparse.ArgumentParser(prog_name, description=__doc__)
    parser.add_argument('fpath', type=str, help='Input file')
    return parser

def entry_point(args=None):
    '''Fake main used to create argparse and call real one'''
    
    if not args: 
        args = []

    parser = create_parser(args[0])
    values = parser.parse_args(args[1:])
    
    try:
        return main(values.fpath)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))