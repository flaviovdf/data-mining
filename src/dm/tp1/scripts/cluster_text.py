# -*- coding: utf8
'''
This code cluster each Pregao based on their description as follows:
    * Transforms descriptions to TF-IDF vector space
    * Runs 10 k means for different values of k
    * Plots the mean intra-cluster-distance / inter-cluster-distance
    * Prints the number of rows in each cluster for each value of k 
'''

from __future__ import division, print_function

from dm.tp1 import tcu_io
from dm.stats.confidence_interval import confidence_interval

from collections import Counter
from matplotlib import pyplot as plt
from scikits.learn.cluster import MiniBatchKMeans
from scikits.learn.feature_extraction.text import Vectorizer
from scikits.learn.metrics import pairwise

import argparse
import numpy as np
import sys
import traceback

def main(tcu_fpath):
    data = tcu_io.load_untreated_csv_to_numpy(tcu_fpath)
    data = data[data['Situacao'] == 'Aceito e Habilitado']
    
    desc_column = data['Descricao']
    des_cmp_column = data['DescricaoComplementar']
    unidade_column = data['UnidadeFornecimento']
    qtd_column = [str(qtd) for qtd in data['Quantidade']]
    
    #Transforms descriptions to base strings
    as_docs = []
    for as_text in zip(desc_column, des_cmp_column, unidade_column, qtd_column):
        doc = " ".join(as_text)
        as_docs.append(doc)

    #Vectorizes to TF-IDF
    vectorizer = Vectorizer()
    doc_sparse_matrix = vectorizer.fit_transform(as_docs)
    
    #Compute clusters
    inter = {}
    intra = {}
    n_runs = 20
    k_vals = range(2, 16)
    for i in xrange(n_runs):
        for k in k_vals:
            #Each K has n_runs clusterings
            inter_array = inter.setdefault(k, np.zeros(n_runs))
            intra_array = intra.setdefault(k, np.zeros(n_runs))
            
            #Run K-Means
            mbkm = MiniBatchKMeans(k, init = 'random')
            mbkm.fit(doc_sparse_matrix)
            
            centers = mbkm.cluster_centers_
            labels = mbkm.labels_
            
            #Inter distance. We use min because the ideia is to maximize this.
            #Min serves as a penalty for worse case.
            dist_centers = pairwise.euclidean_distances(centers)
            min_dist_between_centers = \
                np.min(dist_centers[dist_centers > 0])
            inter_array[i] = min_dist_between_centers

            #Intra distance
            dist_all_centers = mbkm.transform(doc_sparse_matrix)
            intra_dists = []
            for doc_id, cluster in enumerate(labels):
                dist = dist_all_centers[doc_id, cluster]
                intra_dists.append(dist)
            intra_array[i] = np.mean(intra_dists)
            
            #Prints num elements per cluster
            print('Run %d ; k = %d' %(i, k))
            counter = Counter(labels)
            for cluster, population in counter.items():
                print('\tK = %d; Pop = %d' %(cluster, population))
            print()
    
    x = inter.keys()
    y = []
    c = []
    for k in x:
        div = inter[k] / intra[k]
        y.append(np.mean(div))
        c.append(confidence_interval(div, 0.90))
    
    #hack for the zero to apper
    x = [0] + x
    y = [0] + y
    c = [0] + c
    
    ax = plt.gca()
    ax.set_yscale('log')
    ax.set_xticks(range(0, 16))
    plt.ylabel('InterCluster/IntraCluster Ratio')
    plt.xlabel('Number of clusters')
    plt.errorbar(x, y, yerr=c, fmt='bo', markersize=8, elinewidth=2)
    plt.show()
    
def create_parser(prog_name):
    '''
    Creates a parser with the given arguments:
        * `tcu_fpath` a path to the untreated tcu file
    '''
    desc = ''
    parser = argparse.ArgumentParser(prog_name, description=desc)
    
    parser.add_argument('tcu_fpath', type=str,
                        help='A untreated tcu file')
    
    return parser

def entry_point(args=None):
    '''Fake main used to create argparse and call real one'''
        
    if not args: 
        args = []

    parser = create_parser(args[0])
    values = parser.parse_args(args[1:])
    
    try:
        return main(values.tcu_fpath)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))