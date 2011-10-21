# -*- coding: utf8
'''
This scripts filters the original TCU file creating a newer
smaller one. The new file is composed of the columns:

1: Cluster - The cluster of the product sold in the pregao
2: ChavePregao - Id of the pregao
3: UASG - ID of the government organ
4: PregoeiroOficial - The name of the seller
5: AceitoPara_CNPJ - The CNPJ of the winner
6: GanhoPregao - The percentual difference between original value and sold val
7: SuperFaturamento - Determines is the GanhoPregao is over valued
'''

from __future__ import division, print_function

from dm.tp1 import tcu_io

from sklearn.feature_extraction.text import Vectorizer
from sklearn.cluster import MiniBatchKMeans

import argparse
import numpy as np
import sys
import traceback

def invalid(data):
    values_ref = data['ValordeReferencia']
    values_neg = data['ValorNegociado']
    values_gain = data['GanhoPregao']

    computed_gain = (values_ref - values_neg) * 100 / values_ref
    
    i = 0
    return_val = set()
    for actual, computed in zip(values_gain, computed_gain):
        if abs(computed - actual) / actual > 0.01:
            return_val.add(i)
        i += 1
    return return_val

def main(tcu_fpath):
    data = tcu_io.load_untreated_csv_to_numpy(tcu_fpath)
    
    #We only want accepted data
    data = data[data['Situacao'] == 'Aceito e Habilitado']

    #Get invalid lines
    invalids = invalid(data)
    
    #Transforms descriptions to base strings
    desc_column = data['Descricao']
    des_cmp_column = data['DescricaoComplementar']
    unidade_column = data['UnidadeFornecimento']
    qtd_column = [str(qtd) for qtd in data['Quantidade']]
    
    as_docs = []
    for as_text in zip(desc_column, des_cmp_column, unidade_column, qtd_column):
        doc = " ".join(as_text)
        as_docs.append(doc)

    #Vectorizes to TF-IDF
    vectorizer = Vectorizer()
    doc_sparse_matrix = vectorizer.fit_transform(as_docs)
    
    #Run K-Means
    num_clusters = 7
    mbkm = MiniBatchKMeans(num_clusters, init = 'random')
    mbkm.fit(doc_sparse_matrix)
    
    #New labels column, replaces both Descricao columns
    labels_column = mbkm.labels_
    
    #Old columns to keep
    chave_column = data['ChavePregao']
    uasg_column = data['UASG']
    pregoeiro_column = data['PregoeiroOficial']
    aceito_column = data['AceitoPara_CNPJ']
    lance_column = data['PeloMenorLance']
    ref_column = data['ValordeReferencia']
    ganho_column = data['GanhoPregao']
    
    #And a new column Superfaturamento
    super_faturamento = np.ndarray(shape=len(labels_column), dtype = 'S12')
    for i, ganho in enumerate(ganho_column):
        if ganho >= -50: #50% vezes o preco é aceito
            super_faturamento[i] = 'OK'
        elif ganho < -50 and ganho > -500: #Mais que isso é super faturado
            super_faturamento[i] = 'Super'
        elif ganho < -500: #Mais que 5x o valor é foda.
            super_faturamento[i] = 'SuperPlus'
    
    for i in xrange(len(labels_column)):
        if i not in invalids:
            print(labels_column[i], end=',')
            print(chave_column[i], end=',')
            print(uasg_column[i], end=',')
            print(pregoeiro_column[i], end=',')
            print(aceito_column[i], end=',')
            print(lance_column[i], end=',')
            print(ref_column[i], end=',')
            print(ganho_column[i], end=',')
            print(super_faturamento[i])
    
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