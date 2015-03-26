import networkx as nx
import scipy.io as sio
import operator
import random


def top10_btwns(graph):
    """
    Returns 10 nodes with the highest betweeness centrality

    :param graph: networkx graph
    :return: list of tuples as (node_nr, betweeness)
    """
    btw = nx.betweenness_centrality(graph, normalized=True)
    top10 = sorted(btw.iteritems(), key=operator.itemgetter(1), reverse=True)[0:10]
    return top10


def longest_comp_len(graph):
    """
    Returns the length of the longest connected component
    :param graph: networkx graph
    :return: lenght of the longest connected component, int
    """
    return max(map(len, list(nx.connected_components(G))))


# load matrixes through loadmat function from scipy.io
with open("Coactivation_matrix.mat") as filename:
    M = sio.loadmat(filename)

# peel sparse and coordinates matrixes from M dict
coa_mat, coo_mat = M["Coactivation_matrix"], M["Coord"]

# load matrix as a nx graph
G = nx.from_numpy_matrix(coa_mat)

top10_btwns_list = top10_btwns(G)
for node in top10_btwns_list:
    print "%d %f" % node

# print len on the longest connected component
print "Length of the longest connected component: ", longest_comp_len(G)
print
# draw nodes to remove from graph
nodes_to_remove = random.sample(G.nodes(), G.number_of_nodes() / 2)
print "After removing half({0}) of all nodes:".format(G.number_of_nodes() / 2)
# remove nodes from graph
G.remove_nodes_from(nodes_to_remove)

print "Length of the longest connected component: ", longest_comp_len(G)

top10_btwns_list = top10_btwns(G)
for node in top10_btwns_list:
    print "%d %f" % node

# save graph to pajek .net format
nx.write_pajek(G, "coa_matrix.net")