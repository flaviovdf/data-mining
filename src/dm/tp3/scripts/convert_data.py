# -*- coding: utf8
'''
This script converts a LastFM tags file by:
    * converting to lower case
    * removing stopwords
    * stemming
    * removing terms that appear less than a given threshold

The last conversion, removing terms that appear less than a given threshold,
is done for the thresholds: 0, 0.05, 0.1, 0.2. 

Results are saved in the given output folder
'''

from __future__ import division, print_function

from dm.tp3.lastfm_io import vectorize_songs

import argparse
import os
import sys
import traceback

def main(fpath, out_folder, use_idf=True):
    for min_filter in 0, 0.05, 0.1, 0.5:
        folder = os.path.join(out_folder, str(min_filter))
        os.mkdir(folder)
        
        out_fpath_tags = os.path.join(folder, 'tags')
        out_fpath_vocab = os.path.join(folder, 'vocab')
        
        doc_mat, vocabulary = vectorize_songs(fpath, use_idf=use_idf,
                                              bottom_filter=min_filter)
        with open(out_fpath_tags, 'w') as tags_file:
            rows, cols = doc_mat.nonzero()
            last_row = rows[0]
            for row, col in zip(rows, cols):
                if row != last_row:
                    assert row > last_row
                    print(file=tags_file)
                    last_row = row
                    
                print('%d:%.6f'%(col, doc_mat[row, col]), file=tags_file, end=' ')
        
        with open(out_fpath_vocab, 'w') as vocab_file:
            for term in vocabulary:
                term_id = vocabulary[term]
                print(term, term_id, file = vocab_file) 

def create_parser(prog_name):
    parser = argparse.ArgumentParser(prog_name, description=__doc__)
    parser.add_argument('fpath', type=str, help='Input file')
    parser.add_argument('out_folder', type=str,
                        help='Folder to store converted files')
    parser.add_argument('--no_idf', action='store_false', help='Ignore IDF')
    return parser

def entry_point(args=None):
    '''Fake main used to create argparse and call real one'''
    
    if not args: 
        args = []

    parser = create_parser(args[0])
    values = parser.parse_args(args[1:])
    
    try:
        return main(values.fpath, values.out_folder, values.no_idf)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))