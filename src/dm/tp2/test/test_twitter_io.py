# -*- coding: utf8

from __future__ import division, print_function

from dm.tp2.test import TWITTER_FILE
from dm.tp2.twitter_io import cleanup_tweet
from dm.tp2.twitter_io import read_grouped_file
from dm.tp2.twitter_io import read_grouped_iterable

from io import StringIO

import unittest

class TestIO(unittest.TestCase):

    def test_cleanup(self):
        #Um is a stopword
        text = u'um dois #três. quatro, CINCO @SeIs!#bra#bra@joao 1x1 1 x 2 こういう時 rt'
        cleaned = cleanup_tweet(text)
        expected = [u'doi',
                    u'#tr',
                    u'quatr',
                    u'cinc',
                    u'@seis',
                    u'#br',
                    u'#br',
                    u'@joao',
                    u'1x1',
                    u'1x2']
        
        self.assertEqual(expected, cleaned)

    def test_read_fake_file(self):
        text = u'2011-10-08 14:00:00 T0 T1\n' + \
               u'2011-10-08 14:00:05 T2\n' + \
               u'2011-10-08 14:05:00 T3\n' + \
               u'2011-10-08 14:15:00 T4\n' + \
               u'2011-10-08 14:19:59 T5\n' + \
               u'2011-10-09 14:00:00 T6\n'
                              
        sio = StringIO(text)
        data = read_grouped_iterable(sio)
        
        self.assertEqual(4, len(data))
        
    def test_read_grouped_real_file(self):
        data = read_grouped_file(TWITTER_FILE, 0, False)
        self.assertEqual(174171, len(data))

        #There are 24 groups of 5 mins in two hours. But since
        #the very last one becomes a new one (it is after 2h)
        #we have 25.
        data = read_grouped_file(TWITTER_FILE, 300, False)
        self.assertEqual(25, len(data))

if __name__ == "__main__":
    unittest.main()