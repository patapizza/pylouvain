#!/usr/bin/env python3

import math
import unittest
from pylouvain import PyLouvain

class PylouvainTest(unittest.TestCase):

    def test_karate_club(self):
        pyl = PyLouvain.from_file("karate.txt")
        partition, q = pyl.apply_method()
        q_ = q * 10000
        self.assertEqual(4, len(partition))
        self.assertEqual(4298, math.floor(q_))
        self.assertEqual(4299, math.ceil(q_))

    def test_arxiv(self):
        pyl = PyLouvain.from_file("hep-th-citations")
        partition, q = pyl.apply_method()

if __name__ == '__main__':
    unittest.main()
