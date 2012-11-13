#!/usr/bin/env python3

'''
    Implements the Louvain method.
    Input: a weighted undirected graph
    Ouput: a partition whose modularity is maximum
'''
class PyLouvain:

    '''
        Builds a graph from _path.
        _path: a path to a file containing "node_from node_to" edges (one per line)
    '''
    @classmethod
    def from_file(cls, path):
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        nodes = {}
        edges = []
        for line in lines:
            n = line.split()
            nodes[n[0]] = 1
            nodes[n[1]] = 1
            edges.append(((n[0], n[1]), 1))
        print("%d nodes, %d edges" % (len(list(nodes.keys())), len(edges)))
        return cls(list(nodes.keys()), edges)

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
        best_partition = [[node] for node in network[0]]
        while 1:
            # TODO: precompute parameter m (and k vector?)
            partition = [c for c in self.first_phase(network) if c]
            nodes, edges = self.second_phase(network, partition)
            if partition == best_partition:
                break
            best_partition = partition
            network = (nodes, edges)
            print("%s (%.2f)" % (best_partition, self.compute_modularity(network, partition)))
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
        Computes the modularity gain of having node in community _c.
        _node: an int
        _c: an int
        _network: a (nodes, edges) pair
        _partition: a list of lists of nodes
    '''
    def compute_modularity_gain(self, node, c, network, partition):
        # TODO: precompute m and k_i
        m, s_in, s_tot, k_i, k_i_in = 0, 0, 0, 0, 0
        for edge in network[1]:
            c0 = self.get_community(edge[0][0], partition)
            c1 = self.get_community(edge[0][1], partition)
            # compute m (sum of the weights of all the links in the network)
            m += edge[1]
            # compute s_in (sum of the weights of the links inside _c)
            if c0 == c and c1 == c:
                s_in += edge[1]
            # compute s_tot (sum of the weights of the links incident to nodes in _c)
            if c0 == c or c1 == c:
                s_tot += edge[1]
            # compute k_i (sum of the weights of the links incident to _node)
            if edge[0][0] == node or edge[0][1] == node:
                k_i += edge[1]
            # compute k_i,in (sum of the weights of the links from _node to nodes in _c)
            if edge[0][0] == node and c1 == c or edge[0][1] == node and c0 == c:
                k_i_in += edge[1]
        m2 = 2 * m
        s_tot_k_i = (s_tot + k_i) / m2
        s_tot_ = s_tot / m2
        k_i_ = k_i / m2
        return ((s_in + k_i_in) / m2 - s_tot_k_i * s_tot_k_i) - (s_in / m2 - s_tot_ * s_tot_ - k_i_ * k_i_)

    '''
        Computes the sum of the weights of the edges incident to vertex _i.
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
        # make initial partition
        best_partition = [[node] for node in network[0]]
        while 1:
            improvement = False
            for node in network[0]:
                node_community = self.get_community(node, best_partition)
                # default best community is its own
                best_community = node_community
                best_gain = 0
                # remove _node from its community
                partition = [[pp for pp in p] for p in best_partition]
                partition[best_community].remove(node)
                # TODO: only consider neighbors from different communities
                for neighbor in self.get_neighbors(node, network[1]):
                    community = self.get_community(neighbor, best_partition)
                    # compute modularity gain obtained by moving _node to the community of _neighbor
                    gain = self.compute_modularity_gain(node, community, network, partition)
                    if gain > best_gain:
                        best_community = community
                        best_gain = gain
                # insert _node into the community maximizing the modularity gain
                partition[best_community].append(node)
                best_partition = partition
                if node_community != best_community:
                    improvement = True
            if not improvement:
                break
        return best_partition

    '''
        Returns the community in which _node is (among _partition).
        _node: an int
        _partition: a list of lists of nodes
    '''
    def get_community(self, node, partition):
        # TODO: use of an efficient data structure to retrieve one's community
        for i in range(len(partition)):
            if node in partition[i]:
                return i
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
        Performs the second phase of the method.
        _network: a (nodes, edges) pair
        _partition: a list of lists of nodes
    '''
    def second_phase(self, network, partition):
        nodes_ = [i for i in range(len(partition))]
        edges_ = {}
        for e in network[1]:
            ci = self.get_community(e[0][0], partition)
            cj = self.get_community(e[0][1], partition)
            # TODO? add constraint ci < cj
            try:
                edges_[(ci, cj)] += e[1]
            except KeyError:
                edges_[(ci, cj)] = e[1]
        edges_ = [(k, v) for k, v in edges_.items()]
        return (nodes_, edges_)

