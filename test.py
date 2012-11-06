#!/usr/bin/env python3

import unittest
from pylouvain import PyLouvain

class PylouvainTest(unittest.TestCase):

    def setUp(self):
        self.nodes = [i for i in range(10)]
        self.edges = [((0, 4), 22),
                 ((0, 1), 24),
                 ((1, 4), 12),
                 ((3, 1), 1),
                 ((3, 6), 1),
                 ((6, 7), 1),
                 ((7, 9), 1),
                 ((6, 9), 1),
                 ((3, 2), 1),
                 ((5, 8), 11),
                 ((8, 2), 11),
                 ((5, 2), 11)]
        self.pyl = PyLouvain(self.nodes, self.edges)

    def test_modularity(self):
        print("%.2f\n" % self.pyl.compute_modularity((self.nodes, self.edges), [[i] for i in range(10)]))

    def test_method(self):
        print(self.pyl.apply_method())

if __name__ == '__main__':
    unittest.main()
