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
        # TODO: handle "node_from node_to weight" format
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        nodes = {}
        edges = []
        for line in lines:
            n = line.split()
            nodes[int(n[0])] = 1
            nodes[int(n[1])] = 1
            edges.append(((int(n[0]), int(n[1])), 1))
        # rebuild graph with successive identifiers
        nodes = list(nodes.keys())
        nodes.sort()
        i = 0
        nodes_ = []
        d = {}
        for n in nodes:
            nodes_.append(i)
            d[n] = i
            i += 1
        edges_ = []
        for e in edges:
            edges_.append(((d[e[0][0]], d[e[0][1]]), e[1]))
        print("%d nodes, %d edges" % (len(nodes_), len(edges_)))
        return cls(nodes_, edges_)

    '''
        Initializes the method.
        _nodes: a list of ints
        _edges: a list of ((int, int), weight) pairs
    '''
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        # precompute m2 (2 * sum of the weights of all links in network)
        #            k_i (sum of the weights of the links incident to node i)
        self.m2 = 0
        self.k_i = [0 for n in nodes]
        self.edges_of_node = {}
        for e in edges:
            self.m2 += e[1]
            self.k_i[e[0][0]] += e[1]
            self.k_i[e[0][1]] += e[1]
            # save edges by node
            if e[0][0] not in self.edges_of_node:
                self.edges_of_node[e[0][0]] = [e]
            else:
                self.edges_of_node[e[0][0]].append(e)
            if e[0][1] not in self.edges_of_node:
                self.edges_of_node[e[0][1]] = [e]
            elif e[0][0] != e[0][1]:
                self.edges_of_node[e[0][1]].append(e)
        self.m2 *= 2
        # access community of a node in O(1) time
        self.communities = [n for n in nodes]


    '''
        Applies the Louvain method.
    '''
    def apply_method(self):
        network = (self.nodes, self.edges)
        best_partition = [[node] for node in network[0]]
        i = 1
        while 1:
            print("pass #%d" % i)
            i += 1
            partition = [c for c in self.first_phase(network) if c]
            if partition == best_partition:
                break
            network = self.second_phase(network, partition)
            best_partition = partition
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
                if self.communities[i] != self.communities[j]:
                    continue
                q += self.get_weight(i, j, network[1]) - (self.compute_weights(i, network[1]) * self.compute_weights(j, network[1]) / m)
        return q / m

    '''
        Computes the modularity gain of having node in community _c.
        _node: an int
        _c: an int
        _k_i_in: the sum of the weights of the links from _node to nodes in _c
        _edges: a list of ((node, node), weight) pairs
        _partition: a list of lists of nodes
    '''
    def compute_modularity_gain(self, node, c, k_i_in):
        s_tot_k_i = (self.s_tot[c] + self.k_i[node]) / self.m2
        s_tot_ = self.s_tot[c] / self.m2
        k_i_ = self.k_i[node] / self.m2
        return ((self.s_in[c] + k_i_in) / self.m2 - s_tot_k_i * s_tot_k_i) - (self.s_in[c] / self.m2 - s_tot_ * s_tot_ - k_i_ * k_i_)

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
        best_partition = self.make_initial_partition(network)
        while 1:
            improvement = False
            for node in network[0]:
                node_community = self.communities[node]
                # default best community is its own
                best_community = node_community
                best_gain = 0
                # remove _node from its community
                best_partition[node_community].remove(node)
                self.communities[node] = -1
                self.s_in[node_community] -= self.k_i[node]
                self.s_tot[node_community] -= self.k_i[node]
                communities = {} # only consider neighbors of different communities
                for neighbor in self.get_neighbors(node):
                    community = self.communities[neighbor]
                    if community in communities:
                        continue
                    communities[community] = 1
                    k_i_in = 0
                    for e in self.edges_of_node[node]:
                        if e[0][0] == node and self.communities[e[0][1]] == community or e[0][1] == node and self.communities[e[0][0]] == community:
                            k_i_in += e[1]
                    # compute modularity gain obtained by moving _node to the community of _neighbor
                    gain = self.compute_modularity_gain(node, community, k_i_in)
                    if gain > best_gain:
                        best_community = community
                        best_gain = gain
                # insert _node into the community maximizing the modularity gain
                best_partition[best_community].append(node)
                self.communities[node] = best_community
                self.s_in[best_community] += self.k_i[node]
                self.s_tot[best_community] += self.k_i[node]
                if node_community != best_community:
                    improvement = True
            if not improvement:
                break
        return best_partition

    '''
        Yields the nodes adjacent to _node.
        _node: an int
    '''
    def get_neighbors(self, node):
        for e in self.edges_of_node[node]:
            if e[0][0] == node and e[0][1] == node:
                continue # a node is not a neighbor of itself
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
        Builds the initial partition from _network.
        _network: a (nodes, edges) pair
    '''
    def make_initial_partition(self, network):
        partition = [[node] for node in network[0]]
        self.s_in = [0 for node in network[0]]
        self.s_tot = [self.k_i[node] for node in network[0]]
        for e in network[1]:
            if e[0][0] == e[0][1]: # only self-loops
                self.s_in[e[0][0]] += e[1]
        return partition

    '''
        Performs the second phase of the method.
        _network: a (nodes, edges) pair
        _partition: a list of lists of nodes
    '''
    def second_phase(self, network, partition):
        nodes_ = [i for i in range(len(partition))]
        # relabelling communities
        communities_ = []
        d = {}
        i = 0
        for community in self.communities:
            if community in d:
                communities_.append(d[community])
            else:
                d[community] = i
                communities_.append(i)
                i += 1
        self.communities = communities_
        # building relabelled edges
        edges_ = {}
        for e in network[1]:
            ci = self.communities[e[0][0]]
            cj = self.communities[e[0][1]]
            try:
                edges_[(ci, cj)] += e[1]
            except KeyError:
                edges_[(ci, cj)] = e[1]
        edges_ = [(k, v) for k, v in edges_.items()]
        # recomputing k_i vector and storing edges by node
        self.k_i = [0 for n in nodes_]
        self.edges_of_node = {}
        for e in edges_:
            self.k_i[e[0][0]] += e[1]
            if e[0][0] != e[0][1]: # counting self-loops only once
                self.k_i[e[0][1]] += e[1]
            if e[0][0] not in self.edges_of_node:
                self.edges_of_node[e[0][0]] = [e]
            else:
                self.edges_of_node[e[0][0]].append(e)
            if e[0][1] not in self.edges_of_node:
                self.edges_of_node[e[0][1]] = [e]
            elif e[0][0] != e[0][1]:
                self.edges_of_node[e[0][1]].append(e)
        # resetting communities
        self.communities = [n for n in nodes_]
        return (nodes_, edges_)

