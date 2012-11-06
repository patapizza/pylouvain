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
        network = (self.nodes, self.edges)
        best_partition = self.make_initial_partition(network[0])
        i = 1
        while 1:
            print("pass #%d" % i)
            i += 1
            # TODO: precompute parameter m (and k vector?)
            partition = [c for c in self.first_phase(network) if c]
            nodes, edges = self.second_phase(network, partition)
            if partition == best_partition:
                break
            best_partition = partition
            network = (nodes, edges)
            print(best_partition)
        return best_partition

    '''
        Computes the modularity of _network.
        _network: a (nodes, edges) pair
        _partition: a list of lists of nodes
    '''
    def compute_modularity(self, network, partition):
        # compute m
        m = 0
        for e in network[1]:
            m += e[1]
        q = 0
        for i in network[0]:
            for j in network[0]:
                if self.get_community(i, partition) != self.get_community(j, partition):
                    continue
                q += self.get_weight(i, j, network[1]) - (self.compute_weights(i, network[1]) * self.compute_weights(j, network[1]) / m)
        return q / m

    '''
        Computes the sum of the weights of the edges attached to vertex _i.
        _i: a node
        _edges: a list of ((node, node), weight) pairs
    '''
    def compute_weights(self, i, edges):
        w = 0
        for e in edges:
            if e[0][0] == i:
                w += e[1]
        return w

    '''
        Performs the first phase of the method.
        _network: a (nodes, edges) pair
    '''
    def first_phase(self, network):
        partition = self.make_initial_partition(network[0])
        best_partition = (self.compute_modularity(network, partition), partition)
        while 1:
            best_modularity = best_partition[0]
            for node in network[0]:
                for neighbor in self.get_neighbors(node, network[1]):
                    # move _node from its community to the community of _neighbor
                    current_partition = [[pp for pp in p] for p in partition]
                    current_partition[self.get_community(node, partition)].remove(node)
                    current_partition[self.get_community(neighbor, partition)].append(node)
                    # compute modularity obtained
                    current_modularity = self.compute_modularity(network, current_partition)
                    if best_partition[0] < current_modularity:
                        best_partition = (current_modularity, current_partition)
                # move node from its community to the one of the neighbor maximizing the modularity gain (if positive)
                partition = best_partition[1]
            if best_partition[0] == best_modularity: # no improvement
                break
        return partition

    '''
        Returns the community in which _node is (among _partition).
        _node: an int
        _partition: a list of lists of nodes
    '''
    def get_community(self, node, partition):
        for i in range(len(partition)):
            if node in partition[i]:
                return i
        print("unable to find community of node %d" % node)
        return -1

    '''
        Yields the nodes adjacent to _node.
        _node: an int
        _edges: a list of ((node, node), weight) pairs
    '''
    def get_neighbors(self, node, edges):
        for e in edges:
            if e[0][0] == node:
                yield e[0][1]
            if e[0][1] == node:
                yield e[0][0]

    '''
        Returns the weight of edge (_i, _j) among _edges.
        _i: a node
        _j: a node
        _edges: a list of ((node, node), weight) pairs
    '''
    def get_weight(self, i, j, edges):
        for e in edges:
            if e[0][0] == i and e[0][1] == j:
                return e[1]
        return 0

    '''
        Builds the initial partition.
        _nodes: list of ints
    '''
    def make_initial_partition(self, nodes):
        return [[node] for node in nodes]

    '''
        Performs the second phase of the method.
        _network: a (nodes, edges) pair
        _partition: a list of lists of nodes
    '''
    def second_phase(self, network, partition):
        nodes_new = [i for i in range(len(partition))]
        edges_new = []
        for e in network[1]:
            ci = self.get_community(e[0][0], partition)
            cj = self.get_community(e[0][1], partition)
            edges_new.append(((ci, cj), e[1]))
        # TODO: flatten edges_new using a dict
        return (nodes_new, edges_new)

