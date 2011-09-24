# -*- coding: utf8
'''Functions to read the input file clean it up.'''

from __future__ import division, print_function

import io
import nltk
import time
import re
import unicodedata

#Regular expression for input file
FMT_RE = r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)\s+(.*)'
MATCHER = re.compile(FMT_RE)

#Time format in iput files
TIME_FMT = '%Y-%m-%d %H:%M:%S'

#This regular expression filters words, hashtags and mentions
VALID_TOLENS_RE = r'\d\sx\s\d|\w+|#\w+|@\w+'

def strip_accents(tweet):
    '''Auxiliary method for stripping accents from a string'''
    
    utweet = unicode(tweet)
    norm = unicodedata.normalize('NFKD', utweet).encode('ASCII', 'ignore')
    return unicode(norm)
    
def cleanup_tweet(tweet):
    '''
    The tweet is cleaned up in the following manner:
      1. We filter out valid words (or tokens) based on a regex which captures:
         words composed of [a-z0-9]*, hashtags, mentions, scores (e.g. 1 x 0)
      2. After this initial filter, we filter out portuguese stopwords + 'rt'
      3. Then we stem words.
      4. Lastly, we strip accents
    '''
    
    tokenizer = nltk.RegexpTokenizer(VALID_TOLENS_RE)
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    stopwords.add('rt') #RETWEET
    stemmer = nltk.stem.RSLPStemmer()
    
    document = []
    for word in tokenizer.tokenize(tweet):
        toadd = word.lower()
        if toadd not in stopwords:
            if '@' not in toadd:
                toadd = stemmer.stem(toadd)
                toadd = strip_accents(toadd)
            
            #The replace is used for scores such as: '1   x 2' -> '1x2'
            toadd = toadd.replace(' ', '')
            if len(toadd) > 0: #Some japanese characters end up with 0 len.
                document.append(toadd)
            
    return document

#We can make this a generator to save mem, but the file is really small.
def read_grouped_iterable(input_iterable, group_time_secs = 300,
                          clean = True):
    '''
    Reads and groups tweets according to a time interval. If `clean` is
    true, this method will also invoke `cleanup_tweet` for each tweet.
    
    Arguments
    ---------
    
    input_iterable: an interable of strings
        Each string is a tweet preceded by a time stamp
    
    group_time_secs: int
        The interval to group tweets by
    
    clean: bool
        Indicates if data should be cleaned
    '''
    
    grouped_tweets = []
    
    current_group = None
    current_group_time = -group_time_secs
    for line in input_iterable:
        match = MATCHER.match(line)
        assert match
        
        time_str = match.group(1)
        text = match.group(2)
        
        time_stmp = time.strptime(time_str, TIME_FMT)
        time_secs = time.mktime(time_stmp)
        
        delta = time_secs - current_group_time
        if delta >= group_time_secs: #New group
            if current_group:
                grouped_tweets.append(current_group)
            
            current_group_time = time_secs
            current_group = []
        
        if clean:
            doc = cleanup_tweet(text)
            if len(doc) > 0:
                current_group.append(doc)
        else:
            current_group.append(text)
            
    #Last group
    if current_group:
        grouped_tweets.append(current_group)
    
    return grouped_tweets

def read_grouped_file(fname, group_time_secs = 300,
                      clean = True):
    '''
    Reads and groups tweets according to a time interval. If `clean` is
    true, this method will also invoke `cleanup_tweet` for each tweet.
    
    Arguments
    ---------
    
    fname: a path to a file with a tweet per line
        Each string is a tweet preceded by a time stamp
    
    group_time_secs: int
        The interval to group tweets by
    
    clean: bool
        Indicates if data should be cleaned
    '''
     
    with io.open(fname) as input_file:
        return read_grouped_iterable(input_file, group_time_secs, clean)