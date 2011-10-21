# -*- coding: utf8
'''
This script basically does the magic. Almost of the TP is here.
TODO: Improve comment
'''

from __future__ import division, print_function

from collections import Counter
from collections import defaultdict

from dm.tp3.lastfm_io import read_vocabuary
from dm.tp3.lastfm_io import read_sparse

from matplotlib import pyplot as plt

from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import RandomizedPCA
from sklearn.metrics import pairwise_distances, pairwise_kernels

from vod import entropy

import argparse
import numpy as np
import sys
import traceback

def top_10_frequency(data):
    '''
    This gets the top 10 most popular tags in a dataset.
    '''
    cols = data.nonzero()[1]
    freqs = defaultdict(int)
    for term_id in cols:
        freqs[term_id] += 1
    
    inv_freq = defaultdict(list)
    for term_id in freqs:
        freq = freqs[term_id]
        inv_freq[freq].append(term_id)
        

    top_10 = []
    top_freqs = iter(sorted(inv_freq, reverse=True))
    while len(top_10) < 10:
        try:
            freq = next(top_freqs)
            terms = inv_freq[freq]
            top_10.extend(terms)
        except StopIteration:
            break
    
    return top_10[:10]

def run_n_kmeans(data, num_cluster, n_runs, min_count):
    '''
    Run's k means `n_runs` times. Each song is assigned to the
    cluster which happens at least `min_count` of the `n_runs`. 
    If `min_count` is not met, we consider the song as not belonging
    to any cluster.
    '''
    
    #TODO: refactor and move this method to vod common libs
    n_rows = data.shape[0]
    results = np.zeros((n_rows, n_runs))
    kmeans = MiniBatchKMeans(num_cluster)
    
    for i in xrange(n_runs):
        kmeans.fit(data)
        labels_column = kmeans.labels_
        results[:,i] = labels_column
        
    return_val = np.zeros(n_rows)
    for i in xrange(n_rows):
        counter = Counter(results[i])
        most_common = counter.most_common(1)[0]
        clust = most_common[0]
        freq = most_common[1]
        
        if freq > min_count:
            return_val[i] = clust
        else:
            return_val[i] = -1
                    
    return return_val


def compute_probs(song_matrix, num_cluster, labels_column, counter):
    '''
    Computes and returns:
    
    * The probability of a cluster given a tag p(C|t)
    * The probability of a tag given a cluster p(T|c)
    * The probability of a tags given a cluster p(T)
    '''
    #Computing frequencies
    joint_freq = defaultdict(lambda:defaultdict(int))
    tag_freq = defaultdict(int)
    rows, cols = song_matrix.nonzero()
    for row, tag in zip(rows, cols):
        clust = labels_column[row]
        joint_freq[tag][clust] += 1
        tag_freq[tag] += 1

    #Probabilities    
    prob_Ct = defaultdict(lambda:np.zeros(num_cluster))
    prob_Tc = defaultdict(lambda:np.zeros(len(tag_freq)))
    prob_T = np.zeros(len(tag_freq))
    sum_tf = sum(tag_freq.values())
    for tag in tag_freq:
        prob_T[tag] = tag_freq[tag] / sum_tf
        for clust in xrange(num_cluster):
            prob_Ct[tag][clust] = joint_freq[tag][clust] / tag_freq[tag]
            prob_Tc[clust][tag] = joint_freq[tag][clust] / counter[clust]
    
    return prob_Ct, prob_Tc, prob_T

def _summarize(data, vocabulary, labels_column, num_cluster):
    #Basic stats
    print('Number of songs per cluster')
    counter = Counter(labels_column)
    print(counter)
    print()
    
    prob_Ct, prob_Tc, prob_T = compute_probs(data, num_cluster, labels_column, 
                                            counter)
    all_tags = range(len(prob_T))
    
    print('Top tags per cluster')
    for clust in xrange(num_cluster):
        print(clust, 'tags with max_freq_in_cluster')
        songs_in_cluster = np.where(labels_column == clust)[0]
        for tag in top_10_frequency(data[songs_in_cluster]):
            print('\t', vocabulary[tag])
        print()
        
        print(clust, 'tags with max_prob_p(c|t)')
        sort_func = lambda to_sort: prob_Ct[to_sort][clust]
        for tag in sorted(all_tags, key=sort_func, reverse=True)[:10]:
            print('\t', vocabulary[tag])
        print()
    print()
    
    print('Term entropies for each cluster')
    term_entropies = []
    for clust in xrange(num_cluster):
        h =  entropy.entropy(prob_Tc[clust])
        term_entropies.append(h)
        print(clust, h)
    print()
    
    #Number of shared tags between clusters
    X = np.zeros((num_cluster, len(all_tags)))
    for clust in xrange(num_cluster):
        for tag in all_tags:
            X[clust][tag] = prob_Tc[clust][tag]
            
    distances = pairwise_kernels(X)
    for i in xrange(num_cluster):
        distances[i, i] = 0
        
    plt.imshow(distances, cmap='bone_r', interpolation='nearest')
    ax = plt.gca()
    plt.xticks(np.arange(0,num_cluster))
    plt.yticks(np.arange(0,num_cluster))
    plt.colorbar()
    plt.title('Confusion Matrix for Cluster Similarities')
    plt.ylabel('ClusterID')
    plt.xlabel('ClusterID')
    for i in xrange(num_cluster):
        ax.annotate('%.3f'%term_entropies[i], xy=(i, i), 
                    horizontalalignment='center',
                    verticalalignment='center')
    plt.show()
    
    print('Mean difference')
    to_corr_1 = []
    to_corr_2 = []
    for clust in xrange(num_cluster):
        to_corr_1.append(term_entropies[clust])
        to_corr_2.append(np.mean(distances[clust]))
        print(clust, term_entropies[clust], np.mean(distances[clust]))
    from scipy.stats import pearsonr
    print('R2 ', pearsonr(to_corr_1, to_corr_2))
    
#    #Computes the cluster which maximizes p(C|t) for each tag.
#    mle_cluster = np.zeros(num_cluster)
#    for tag in all_tags:
#        most_likely = 0
#        max_joint = 0
#        for clust in xrange(num_cluster):
#            if probs_clust_tag[tag][clust] > max_joint:
#                most_likely = clust
#                max_joint = probs_clust_tag[tag][clust]
#        mle_cluster[tag] = most_likely
#        
##    print('Tags with maximum mutual information')
##    for tag in np.argsort(mutual_info)[::-1][:20]:
##        print(vocabulary[tag], mutual_info[tag], mle_cluster[tag])
##    print()
##    
##    print('Tags with minimum entropies')
##    for tag in np.argsort(entropies)[:20]:
##        print(vocabulary[tag], entropies[tag], mle_cluster[tag])
      
def main(fpath, vocab_fpath, num_cluster, pca):
    song_matrix = read_sparse(fpath)
    vocab = read_vocabuary(vocab_fpath)
    
    data = None
    if not pca:
        data = song_matrix
    else:
        pca_algo = RandomizedPCA(n_components=pca)
        data = pca_algo.fit(song_matrix).transform(song_matrix)
    
    labels_column = run_n_kmeans(data, num_cluster, num_cluster, 2)
    _summarize(song_matrix, vocab, labels_column, num_cluster)
    
def create_parser(prog_name):
    parser = argparse.ArgumentParser(prog_name, __doc__)
    parser.add_argument('fpath', type=str,
                        help='Input file')
    parser.add_argument('vocab_fpath', type=str,
                        help='Vocabulary file')
    parser.add_argument('num_clusters', type=int,
                        help='Number of clusters to use')
    parser.add_argument('--pca', type=int,
                        help='Use pca with this number of components')
    return parser

def entry_point(args=None):
    '''Fake main used to create argparse and call real one'''
    
    if not args: 
        args = []

    parser = create_parser(args[0])
    values = parser.parse_args(args[1:])
    
    try:
        return main(values.fpath, values.vocab_fpath, values.num_clusters,
                    values.pca)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))