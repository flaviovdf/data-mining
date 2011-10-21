# -*- coding: utf8
'''
This script plots a scatter plot with the two first
principal components of the data_set. This plot can be used
to visually determine the number of clusters.
'''
from __future__ import division, print_function

from dm.tp3.lastfm_io import read_sparse
from matplotlib import cm
from matplotlib import pyplot as plt
from sklearn.decomposition.pca import RandomizedPCA

import argparse
import sys
import traceback

def main(fpath, hex):
    song_matrix = read_sparse(fpath)

    pca = RandomizedPCA(n_components = 2)
    pcas = pca.fit(song_matrix).transform(song_matrix)
    
    print(pca.explained_variance_ratio_)
    if hex:
        plt.hexbin(pcas[:,0], pcas[:,1], cmap=cm.get_cmap('bone_r', 100),
                   bins='log', gridsize=100, mincnt=2)
        plt.colorbar()
    else:
        plt.scatter(pcas[:,0], pcas[:,1])
        
    plt.legend()
    ax = plt.gca()
    plt.ylabel('Second Principal Component')
    plt.xlabel('First Principal Component')
    plt.title('PCA of the LastFM dataset')
    
    plt.show()

def create_parser(prog_name):
    desc = __doc__
    parser = argparse.ArgumentParser(prog_name, description=desc)
    parser.add_argument('fpath', type=str, help='Input file')
    parser.add_argument('--hex', action='store_true')     
    return parser

def entry_point(args=None):
    '''Fake main used to create argparse and call real one'''
    
    if not args: 
        args = []

    parser = create_parser(args[0])
    values = parser.parse_args(args[1:])
    
    try:
        return main(values.fpath, values.hex)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))