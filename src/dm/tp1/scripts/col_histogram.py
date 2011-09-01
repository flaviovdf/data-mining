# -*- coding: utf8
'''
Computes histogram for columns of data in the TCU file. Some treatments are 
made:

* If the column contains strings, 'N/A' are masked out. Histogram for strings
  is simply based on counting the occurences of the string.
* If the column contains numbers, we use numpy's hist method. NaNs are masked
  out.
''' 

from __future__ import division, print_function

from dm.tp1 import tcu_io
from dm.stats.curves import ecdf, categorical_hist

from matplotlib import pyplot as plt
from numpy import ma

import argparse
import sys
import traceback

def main(tcu_fpath, col_name):
    data = tcu_io.load_untreated_csv_to_numpy(tcu_fpath)
    
    column = data[col_name]
    dtype = column.dtype
    
    masked = None
    if dtype == 'i' or dtype == 'f':
        masked = ma.masked_invalid(column)
        
        x, y = ecdf(masked)
        plt.plot(x, y, 'bo')
        plt.show()
        
    else:
        #Simple hack for the string case. 
        #Creates a copy with masked values deleted. 
        masked = column[column != 'N/A']
        
        cat, y = categorical_hist(masked)
        
        x = range(1, len(cat) + 1)
        plt.bar(x, y, width = 0.5)
        plt.xticks(x, cat)
        plt.show()

def create_parser(prog_name):
    '''
    Creates a parser with the given arguments:
        * `tcu_file` a path to the untreated tcu file
        * `col_name` the name of the column to compute the histogram
    '''
    desc = ''
    parser = argparse.ArgumentParser(prog_name, description=desc)
    
    parser.add_argument('tcu_fpath', type=str,
                        help='A untreated tcu file')

    parser.add_argument('col_name', type=str,
                        help='Column to compute histogram')
    
    return parser

def entry_point(args=None):
    '''Fake main used to create argparse and call real one'''
    
    if not args: 
        args = []

    parser = create_parser(args[0])
    values = parser.parse_args(args[1:])
    
    try:
        return main(values.tcu_fpath, values.col_name)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))