#!/usr/bin/env python3

import unittest
from pylouvain import PyLouvain

class PylouvainTest(unittest.TestCase):

    def setUp(self):
        self.nodes = [i for i in range(10)]
        self.edges = [((0, 4), 1),
                 ((0, 1), 1),
                 ((1, 4), 1),
                 ((3, 1), 1),
                 ((3, 6), 1),
                 ((6, 7), 1),
                 ((7, 9), 1),
                 ((6, 9), 1),
                 ((3, 2), 1),
                 ((5, 8), 1),
                 ((8, 2), 1),
                 ((5, 2), 1)]
        self.pyl = PyLouvain(self.nodes, self.edges)

    def test_modularity(self):
        self.assertEqual(-0.16666666666666663, self.pyl.compute_modularity((self.nodes, self.edges), [[i] for i in range(10)]))

    def test_method(self):
        self.assertEqual([[0], [1], [2], [3]], self.pyl.apply_method())

if __name__ == '__main__':
    unittest.main()
