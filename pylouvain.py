#!/usr/bin/env python3

'''
    Implements the Louvain method.
    Input: a weighted undirected graph
    Ouput: a partition whose modularity is maximum
'''
class PyLouvain:

    '''
        Initializes the method.
        _network: a (nodes, edges) pair
    '''
    def __init__(self, network):
        self.nodes = network[0]
        self.edges = network[1]

    '''
        Initializes the method.
        _nodes: a list of ints
        _edges: a list of ((int, int), weight) pairs
    '''
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    '''
        Applies the Louvain method.
    '''
    def apply_method(self):
        partition = self.make_initial_partition()
        best_partition = partition
        while 1:
            partition = self.first_phase(partition)
            partition = self.second_phase(partition)
            if partition == best_partition:
                break
            best_partition = partition
        return best_partition

    '''
        Computes the modularity of _network.
        _network: a (nodes, edges) pair
    '''
    def compute_modularity(self, network):
        pass

    '''
        Performs the first phase of the method.
        _partition: a list of lists of nodes
    '''
    def first_phase(self, partition):
        best_modularity = 0
        while 1:
            for node in nodes:
                for neighbor in self.get_neighbors(node):
                    # move node from its partition to the partition of neighbor
                    # compute modularity obtained
                # move node from its partition to the one of the neighbor maximizing the modularity gain (if positive)
            if current_modularity == best_modularity: # no improvement
                break

    '''
        Builds the initial partition.
    '''
    def make_initial_partition(self):
        return [[node] for node in self.nodes]

    '''
        Performs the second phase of the method.
        _partition: a list of lists of nodes
    '''
    def second_phase(self, partition):
        pass

