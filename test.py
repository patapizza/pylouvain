#!/usr/bin/env python3

import math
import unittest
from pylouvain import PyLouvain

class PylouvainTest(unittest.TestCase):

    def test_arxiv(self):
        pyl = PyLouvain.from_file("data/arxiv.txt")
        partition, q = pyl.apply_method()

    def test_citations(self):
        pyl = PyLouvain.from_file("data/hep-th-citations")
        partition, q = pyl.apply_method()

    def test_karate_club(self):
        pyl = PyLouvain.from_file("data/karate.txt")
        partition, q = pyl.apply_method()
        q_ = q * 10000
        self.assertEqual(4, len(partition))
        self.assertEqual(4298, math.floor(q_))
        self.assertEqual(4299, math.ceil(q_))

    def test_lesmis(self):
        pyl = PyLouvain.from_gml_file("data/lesmis.gml")
        partition, q = pyl.apply_method()

    def test_polbooks(self):
        pyl = PyLouvain.from_gml_file("data/polbooks.gml")
        partition, q = pyl.apply_method()

if __name__ == '__main__':
    unittest.main()
