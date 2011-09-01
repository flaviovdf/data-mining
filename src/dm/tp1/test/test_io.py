# -*- coding: utf8
'''Tests for the io module'''

from __future__ import division, print_function

from dm.tp1 import tcu_io
from dm.tp1.test import ORIGINAL_TCU_FILE, TREATED_TCU_FILE

import numpy as np
import unittest

class TestTCUIO(unittest.TestCase):
    '''Test class for tcu_io module'''
    
    def test_load_untreated(self):
        '''Checks if all lines are read, if headers are good and
           if N/A were replaced for nan in numeric fields'''
        
        data = tcu_io.load_untreated_csv_to_numpy(ORIGINAL_TCU_FILE)
        self.assertEquals(len(data), 37165)
        
        names = ('ChavePregao', 'UASG', 'PregoeiroOficial', 'Descricao',
                 'DescricaoComplementar', 'Quantidade', 'UnidadeFornecimento',
                 'ValordeReferencia', 'Situacao', 'AceitoPara','PeloMenorLance',
                 'ValorNegociado', 'GanhoNegociacao', 'GanhoPregao', 
                 'AceitoPara_CNPJ')
        
        expected_num_nas = 0
        with open(ORIGINAL_TCU_FILE) as tcu_file:
            for line in tcu_file:
                spl = line.split(',')
                for token in spl:
                    if token.strip() == 'N/A':
                        expected_num_nas += 1
        
        actual_num_nas = 0
        for column_name in names:         
            self.assertEquals(len(data[column_name]), 37165)
            
            atype = data[column_name].dtype
            if atype != 'i' and atype != 'f':
                matching = data[column_name] == 'N/A'
            else:
                matching = np.isnan(data[column_name])
                
            actual_num_nas += len(data[column_name][matching])
        
        self.assertEquals(expected_num_nas, actual_num_nas)
    
    def test_load_treated(self):
        data = tcu_io.load_treated_csv_to_numpy(TREATED_TCU_FILE)
        self.assertEquals(29202, len(data))

        names = ('Cluster', 'ChavePregao', 'UASG', 'PregoeiroOficial',
                 'AceitoPara_CNPJ', 'PeloMenorLance', 'ValorReferencia', 
                 'GanhoPregao', 'SuperFaturamento')

        for column_name in names:
            self.assertEquals(len(data[column_name]), 29202) 