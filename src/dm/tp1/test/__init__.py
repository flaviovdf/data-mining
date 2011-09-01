'''
Unit tests for the project. This
package also initializes the small files
used for testing. 
'''

import os

DATA_DIR = os.path.join(__path__[0], os.pardir, 'data')

ORIGINAL_DATA_DIR = os.path.join(DATA_DIR, 'original')
ORIGINAL_TCU_FILE = os.path.join(ORIGINAL_DATA_DIR, 'compras.csv')

TREATED_DATA_DIR = os.path.join(DATA_DIR, 'newfmt')
TREATED_TCU_FILE = os.path.join(TREATED_DATA_DIR, 'compras.csv')