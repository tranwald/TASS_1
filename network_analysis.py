#!/usr/bin/python
#  -*- coding: iso-8859-15 -*-

import networkx as nx
import operator
import random
import timeit

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

def print_btwns_table(btwns_list):
    """
    Print table of top10 nodes with highest betweeness centrality

    :param btwns_list: list of tuples as (node_nr, betweeness)
    """
    from prettytable import PrettyTable
    pt = PrettyTable()
    pt.add_column("Node", [x[0] for x in btwns_list])
    pt.add_column("Betweeness Centrality", [x[1] for x in btwns_list])
    pt.padding_width = 1
    pt.float_format = "1.6"
    print "Top10 nodes with the highest betweeness centrality:"
    print pt

# download file with data if not in folder
from os import listdir
if "Coactivation_matrix.mat" not in listdir('.'):
    import urllib
    link = 'https://sites.google.com/site/bctnet/Home/functions/Coactivation_matrix.mat'
    urllib.urlretrieve(link, '"Coactivation_matrix.mat"')

# load matrixes through loadmat function from scipy.io
with open("Coactivation_matrix.mat") as filename:
    import scipy.io as sio
    coa_mat = sio.loadmat(filename)["Coactivation_matrix"]

# peel sparse and coordinates matrixes from M dict
#coa_mat = M["Coactivation_matrix"]

# check if graph is undirected and create graph from matrix
if (coa_mat == coa_mat.transpose()).all():
    G = nx.from_numpy_matrix(coa_mat, create_using=nx.Graph())
    print "Graph is undirected"
else:
    G = nx.from_numpy_matrix(coa_mat, create_using=nx.DiGraph())
    print "Graph is directed"

# add node labels (needed for Pajek)
nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)

# save graph to pajek .net format
nx.write_pajek(G, "coa_matrix.net")

print "\nCalculations made on all nodes ({0}):\n".format(G.number_of_nodes())
# calculate betweeness and print result in table
# prepare timer
setup = '''
from __main__ import longest_comp_len, G
import networkx as nx
'''
# run timer
print timeit.timeit("nx.betweenness_centrality(G, normalized=True)", setup, number=1)
top10_btwns_list = top10_btwns(G)
print_btwns_table(top10_btwns_list)

# print len on the longest connected component
print "\nLength of the longest connected component:", longest_comp_len(G)
print
print timeit.timeit("longest_comp_len(G)", setup, number=1)
# draw nodes to remove from graph
nodes_to_remove = random.sample(G.nodes(), G.number_of_nodes() / 2)

print "\nCalculations after removing half ({0}) of all nodes:\n".format(G.number_of_nodes() / 2)
# remove nodes from graph
G.remove_nodes_from(nodes_to_remove)

# calculate betweeness and print result in table
print timeit.timeit("nx.betweenness_centrality(G, normalized=True)", setup, number=1)
top10_btwns_list = top10_btwns(G)
print_btwns_table(top10_btwns_list)

# print len on the longest connected component
print "\nLength of the longest connected component:", longest_comp_len(G)
print timeit.timeit("longest_comp_len(G)", setup, number=1)
# save graph to pajek .net format
nx.write_pajek(G, "coa_matrix_half.net")

