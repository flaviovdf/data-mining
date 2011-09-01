# -*- coding: utf8
'''
Correlates all pairs of categorical attributes in 
a treated file.
'''
from __future__ import division, print_function

from dm.tp1 import tcu_io
from dm.stats import contingency

from scipy import stats

import argparse
import numpy as np
import sys
import traceback

def main(tcu_fpath):
    data = tcu_io.load_treated_csv_to_numpy(tcu_fpath)
    print(stats.pearsonr(data['ValorReferencia'], data['PeloMenorLance']))
    print(stats.pearsonr(data['ValorReferencia'], data['GanhoPregao']))
    print(stats.pearsonr(data['GanhoPregao'], data['PeloMenorLance']))
    
    to_corr_cat = [('SuperFaturamento', 'PregoeiroOficial'),
                   ('SuperFaturamento', 'AceitoPara_CNPJ'),
                   ('SuperFaturamento', 'Cluster')]
    
    for pair in to_corr_cat:
        row = pair[0]
        col = pair[1]
        
        vals_row = set(data[row])
        vals_col = set(data[col])
        
        n_rows = len(vals_row)
        n_cols = len(vals_col)
        
        #Creating table
        contingency_table = np.ndarray(shape=(n_rows, n_cols), dtype='i')
        for i, possible_row in enumerate(vals_row):
            for j, possible_col in enumerate(vals_col):
                #Create boolean arrays with lines that contain the values
                with_both = \
                    (data[row] == possible_row) & (data[col] == possible_col) 
                num_occur = with_both.sum()
                
                contingency_table[i, j] = num_occur
        
        print('Correlating %s', pair)
        chi2, p, dof, e =  contingency.chi2_contingency(contingency_table)
        
        print('Correlation', pair, ': chi2 = %f; p = %f; df = %f;' \
              %(chi2, p, dof))
        
def create_parser(prog_name):
    '''
    Creates a parser with the given arguments:
        * `tcu_file` a path to the treated tcu file
    '''
    desc = ''
    parser = argparse.ArgumentParser(prog_name, description=desc)
    
    parser.add_argument('tcu_fpath', type=str,
                        help='A treated tcu file')
    
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