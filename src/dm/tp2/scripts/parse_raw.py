# -*- coding: utf8
'''
Parses a raw tweet file and groups it by time. Also, cleans
up tweets.
'''
from __future__ import division, print_function

from dm.tp2.twitter_io import read_grouped_file

import argparse
import io
import os
import sys
import traceback

def main(twitter_fpath, out_folder):
    data = read_grouped_file(twitter_fpath)
    
    for gid, group in enumerate(data):
        with io.open(os.path.join(out_folder, '%d.parsed'%gid), 'w') as outf:
            for document in group:
                outf.write(u'%s\n' % u' '.join(document))

def create_parser(prog_name):
    desc = 'Parses twitter file to generate grouped document files'
    parser = argparse.ArgumentParser(prog_name, description=desc)
    
    parser.add_argument('twitter_fpath', type=str,
                    help='A untreated twitter file')

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
        return main(values.twitter_fpath, values.out_folder)
    except:
        traceback.print_exc()
        parser.print_usage(file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))
