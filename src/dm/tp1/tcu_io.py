# -*- coding: utf-8
'''Common functions used for various scripts'''

from __future__ import division, print_function

import numpy as np

def load_untreated_csv_to_numpy(fname):
    '''
    Loads an untreated TCU file. String "N/A" will 
    become nans. 
    
    Parameters
    ----------
    fname: path to read (str)
        Content to read
    '''
    
    names = ('ChavePregao', 'UASG', 'PregoeiroOficial', 'Descricao',
             'DescricaoComplementar', 'Quantidade', 'UnidadeFornecimento',
             'ValordeReferencia', 'Situacao', 'AceitoPara', 'PeloMenorLance',
             'ValorNegociado', 'GanhoNegociacao', 'GanhoPregao', 
             'AceitoPara_CNPJ')
    
    #527 is the maximum number of chars in a field
    dtype = 'i, i, S527, S527, S527, i, S527, f, S527, S527, f, f, f, f, S527'
    
    data =  np.genfromtxt(fname, names = names, dtype = dtype,  delimiter=',',
                          comments = None, autostrip = True, missing='N/A')
    return data

def load_treated_csv_to_numpy(fname):
    '''
    Loads a treated TCU file. No invalid values exist in these files
    
    Parameters
    ----------
    fname: path to read (str)
        Content to read
    '''
    
    names = ('Cluster', 'ChavePregao', 'UASG', 'PregoeiroOficial',
             'AceitoPara_CNPJ', 'PeloMenorLance', 'ValorReferencia', 
             'GanhoPregao', 'SuperFaturamento')
    
    dtype = 'i, i, i, S527, S527, f, f, f, S527'
    data =  np.genfromtxt(fname, names = names, dtype = dtype,  delimiter=',',
                          comments = None, autostrip = True)
    
    lower = np.core.defchararray.lower
    data['PregoeiroOficial'] = lower(data['PregoeiroOficial'])
    return data
    