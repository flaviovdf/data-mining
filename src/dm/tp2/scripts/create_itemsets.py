# -*- coding: utf8
'''
Given a folder with parsed this tweets, this code will:
    * Convert each parsed file to a itemset file
    * Create a vocabulary file which maps itemids in the itemset
      file to terms.
'''
from __future__ import division, print_function

import argparse
import glob
import io
import os
import sys
import traceback

def main(parsed_folder, out_folder):
    
    for fpath in glob.glob(os.path.join(parsed_folder, '*.parsed')):
        basename = os.path.basename(fpath)
        doc_id = basename.split('.')[0]
        
        vocabulary = {}
        term_id_space = 0
        item_sets = []
        
        with io.open(fpath) as infile:
            for line in infile:
                #First token is lineid
                spl = line.split()
                unique_terms = set(spl)
                
                iset = set()
                for term in unique_terms:
                    if term not in vocabulary:
                        vocabulary[term] = term_id_space
                        term_id_space += 1
                        
                    iset.add(str(vocabulary[term]))
                
                item_sets.append(iset)
        
        #Writes itemset file
        iset_fpath = os.path.join(out_folder, doc_id + '.isets')
        with io.open(iset_fpath, 'w') as isetfile:
            for iset in item_sets:
                isetfile.write(u'%s\n' %' '.join(sorted(iset)))
        
        #Writes vocabulary
        inv_vocab = dict((tid, term) for term, tid in vocabulary.items())
        vocab_fpath = os.path.join(out_folder, doc_id + '.vocab')
        with io.open(vocab_fpath, 'w') as vocabfile:
            for tid in sorted(inv_vocab):
                term = inv_vocab[tid]
                vocabfile.write(u'%s %s\n' %(tid, term))

def create_parser(prog_name):
    desc = 'Converts parsed twitter data to itemsets'
    parser = argparse.ArgumentParser(prog_name, description=desc)
    
    parser.add_argument('parsed_folder', type=str,
                    help='A folder with parsed data')

    parser.add_argument('out_folder', type=str,
                    help='An output folder')

    return parser

def entry_point(args=None):
    '''Fake main used to create argparse and call real one'''
    
    if not args: 
        args = []

    parser = create_parser(args[0])
    values = parser.parse_args(args[1:])
    
    try:
        return main(values.parsed_folder, values.out_folder)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))
