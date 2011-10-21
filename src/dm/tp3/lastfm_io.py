# -*- coding: utf8
'''This module contains the code used for data conversion'''

from __future__ import division, print_function

from collections import defaultdict

from scipy import sparse
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import Vectorizer

import nltk

class NoopAnalyzer(BaseEstimator):
    '''
    Since we use NLTK to preprocess (more control) this
    class is used to bypass sklearns preprocessing
    '''
    def analyze(self, text_document):
        '''Does nothing'''
        return text_document

def __tokenize_and_stem(fpath):
    '''
    Tokenizes and stems the file, converting each line to 
    an array of words.
    
    Arguments
    ---------
    fpath: a path to a file 
        Each line is a song, tags are separated by space
    '''
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    stopwords = set(nltk.corpus.stopwords.words('english'))
    stemmer = nltk.stem.PorterStemmer()
    
    docs = []
    term_pops = defaultdict(int)
    with open(fpath) as lastfm_file:
        for line in lastfm_file:
            as_doc = []
            for term in tokenizer.tokenize(line):
                term = term.lower().strip()
                if term not in stopwords and term != '':
                    stemmed = stemmer.stem(term)
                    as_doc.append(stemmed)
                    term_pops[stemmed] += 1
                    
            if len(as_doc) > 1:
                docs.append(as_doc)

    return docs, term_pops

def clean_up(fpath, bottom_filter=0.005):
    '''
    Converts a LastFM tag file to a series of tokens. This code
    stems the tags, removes stopwords and filters infrequent
    tags (whose probability is bellow `bottom_filter`).
    
    Arguments
    ---------
    fpath: a path to a file 
        Each line is a song, tags are separated by space
    bottom_filter: float (defaults to 0.005, half of one percent)
        Minimum probability for tags to be considered useful
    '''
    docs, term_pops = __tokenize_and_stem(fpath)
    for doc in docs:
        to_yield = []
        for term in doc:
            prob_term = term_pops[term] / len(term_pops)
            if prob_term > bottom_filter:
                to_yield.append(term)
        
        if len(to_yield) > 1:
            yield to_yield
    
def vectorize_songs(fpath, use_idf=False, bottom_filter=0.005):
    '''
    Converts a LastFM tag file to a sparse matrix pondered. We can assign
    weights based on IDF if specified.
    
    Arguments
    ---------
    fpath: a path to a file 
        Each line is a song, tags are separated by space
    use_idf: bool (optinal, defaults to True)
        Indicates whether to use IDF.
    bottom_filter: float (defaults to 0.005, half of one percent)
        Minimum probability for tags to be considered useful
    '''
    #Vectorizes to TF-IDF
    vectorizer = Vectorizer(analyzer=NoopAnalyzer(), use_idf = use_idf)
    sparse_matrix = vectorizer.fit_transform(clean_up(fpath))
    vocabulary = vectorizer.vocabulary
    return sparse_matrix, vocabulary

def read_sparse(fpath):
    '''
    Reads a converted tags file (now in LibSVM sparse format) to
    a sparse matrix.
    
    Arguments
    ---------
    fpath: str
        path to the file
    '''
    as_dict = {}
    num_col = 0
    num_row = 0
    with open(fpath) as sparse_file:
        for line in sparse_file:
            spl = line.split()
            for token in spl:
                col, value = token.split(':')
                col = int(col)
                as_dict[num_row, col] = value
                
                if col > num_col:
                    num_col = col
                    
            num_row += 1
    
    shape = (num_row, num_col + 1)
    return_val = sparse.dok_matrix(shape)
    for row, col in as_dict:
        return_val[row, col] = as_dict[row, col]
    
    return return_val.tocsr()

def read_vocabuary(fpath):
    '''
    Reads a vocabulary file and converts it to a dictionary
    
    Arguments
    ---------
    fpath: str
        path to the file
    '''
    return_val = {}
    with open(fpath) as vocab_file:
        for line in vocab_file:
            spl = line.split()
            key = int(spl[1])
            value = spl[0]
            return_val[key] = value
    return return_val