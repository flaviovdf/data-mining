# -*- coding: utf8
'''
This script plots the BetaCV for cluster sizes of
[3 to 20] + [25] + [35]
'''
from __future__ import division, print_function

from dm.tp3.lastfm_io import read_sparse
from matplotlib import pyplot as plt
from vod.learn.cluster import kmeans_betacv

import argparse
import sys
import traceback

def main(fpath):
    song_matrix = read_sparse(fpath)
    to_plot_x = [0] + range(2, 21) + [25, 35]
    to_plot_y = [0]
    errors = [0]
    for x in to_plot_x[1:]:
        print(x)
        beta_cv, err = kmeans_betacv(song_matrix, x, True)
        to_plot_y.append(beta_cv)
        errors.append(err)
    
    ax = plt.gca()
    ax.set_xticks(to_plot_x)
    plt.ylabel('IntraCluster/InterCluster Ratio')
    plt.xlabel('Number of clusters')
    plt.errorbar(to_plot_x, to_plot_y, yerr=errors, 
                 fmt='bo', markersize=8, elinewidth=2)
    plt.show()

def create_parser(prog_name):
    parser = argparse.ArgumentParser(prog_name, description=__doc__)
    parser.add_argument('fpath', type=str,
                    help='Input file')
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