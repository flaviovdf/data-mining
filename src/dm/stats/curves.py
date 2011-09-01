# -*- coding: utf8
'''
Various statistical functions used by other parts of the code.
'''

from __future__ import division, print_function

from collections import Counter
from scipy.stats import mstats

import numpy as np

def ecdf(data):
    '''
    Computes the Expected CDF of a data array.
    
    Parameters
    ----------
    data: array of numbers
        The data to compute the cdf
    
    Returns
    -------
    Two other arrays corresponding to the x and y axes.
    '''
    
    obs = np.asanyarray(data)
    rank = mstats.rankdata(obs)

    return_val_x = np.unique(obs)
    return_val_y = np.unique(rank) / len(rank)

    return (return_val_x, return_val_y)

def epdf(data, bins=20):
    '''
    Computes the Expected PDF of a data array.
    
    Parameters
    ----------
    data: array of numbers
        The data to compute the cdf
    bins: number of bins
    
    Returns
    -------
    Two other arrays corresponding to the bins and y axes, plus
    a float corresponding to the length of each bin.
    '''
    
    y, ranges = np.histogram(data, bins = bins, normed = True)
    length = ranges[1] - ranges[0]
    x = np.diff(ranges) + ranges[:-1]
    
    return x, y, length

def categorical_hist(data):
    '''
    Computes the histogram of categorical data.
    
    Parameters
    ----------
    data: array of any object
        The data to compute the histogram
    
    Returns
    -------
    Two other arrays corresponding to the categories and y values.
    '''
    
    counter = Counter(data)
    
    x = np.array(counter.keys())
    y = np.array(counter.values())
    y = y / y.sum() 
    
    return x, y