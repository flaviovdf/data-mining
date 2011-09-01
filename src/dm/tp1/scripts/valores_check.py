# -*- coding: utf8
'''
Does some simple sanity checks on dataset. Determines if one CNPJ is used
for more than one person, if gains are correct and if only one CNPJ wan each
Pregao.
'''
from __future__ import division, print_function

from dm.tp1 import tcu_io

from collections import defaultdict
from numpy import ma

import argparse
import sys
import traceback

def main(tcu_fpath):
    data = tcu_io.load_untreated_csv_to_numpy(tcu_fpath)
    data = data[data['Situacao'] == 'Aceito e Habilitado']
    
    #Checks if gain is correct
    values_ref = ma.masked_invalid(data['ValordeReferencia'])
    values_neg = ma.masked_invalid(data['ValorNegociado'])
    values_gain = ma.masked_invalid(data['GanhoPregao'])

    computed_gain = (values_ref - values_neg) * 100 / values_ref
    
    i = 1
    for actual, computed in zip(values_gain, computed_gain):
        if abs(computed - actual) / actual > 0.01:
            print('Invalid line %d' %i, computed, actual)
        i += 1

    #Checks if only one CNPJ exists per person
    aceito_names = data['AceitoPara']
    aceito_cnpj = data['AceitoPara_CNPJ']
    
    uniq_check_cnpj = defaultdict(set)
    for cnpj, name in zip(aceito_cnpj, aceito_names):
        uniq_check_cnpj[cnpj].add(name)
    
    for cnpj in uniq_check_cnpj:
        if len(uniq_check_cnpj[cnpj]) > 1:
            print('Duplicado CNPJ', cnpj, '->')
            for name in uniq_check_cnpj[cnpj]:
                print('\t', name)
    
    #Checks if ChavePregao maps to one cnpj only
    chaves = data['ChavePregao']
    uniq_check_chave = defaultdict(set)
    for chave, cnpj in zip(chaves, aceito_cnpj):
        uniq_check_chave[cnpj].add(cnpj)

    for chave in uniq_check_chave:
        if len(uniq_check_chave[chave]) > 1:
            print('Duplicado CHAVE', chave, '->')
            for cnpj in uniq_check_chave[chave]:
                print('\t', cnpj)

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