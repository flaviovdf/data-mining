# -*- coding: utf8
'''
Computes the collocations for an already parsed tweet file. Collocations
are common *sequences* of words found in the collection.
''' 

from __future__ import division, print_function

import argparse
import nltk
import sys
import traceback

def main(fpath, sup):
    
    with open(fpath) as inputfile:
        docs = []
        for line in inputfile:
            docs.append(line.split())
        
        finder = nltk.collocations.TrigramCollocationFinder.from_documents(docs)
        finder.apply_freq_filter(sup)
        
        measures = nltk.collocations.TrigramAssocMeasures()
        collocations = finder.score_ngrams(measures.raw_freq)
        
        for score, col in collocations:
            print(score, col)

def create_parser(prog_name):
    desc = 'Computes collocations of a parsed text file'
    parser = argparse.ArgumentParser(prog_name, description=desc)
    
    parser.add_argument('fpath', type=str,
                    help='Input file')

    parser.add_argument('sup', type=int,
                    help='Filters collocations with less than sup occurrences')

    return parser

def entry_point(args=None):
    '''Fake main used to create argparse and call real one'''
    
    if not args: 
        args = []

    parser = create_parser(args[0])
    values = parser.parse_args(args[1:])
    
    try:
        return main(values.fpath, values.sup)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))