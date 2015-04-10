#!/usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from math import log10
from scipy.stats import binned_statistic

# load graph from file
with open("coa_matrix.net") as filename:
    G = nx.read_pajek(filename)

# get nodes degrees and degree frequencies
nodes_degree = G.degree()
cd = [(k,v) for k,v in Counter(nodes_degree.values()).iteritems()]
d, f = list(zip(*cd))
d = map(float, d)
f = [x/float(sum(f)) for x in f]

# calculate log bins
max_base = max(log10(max(d)), log10(max(f)))
min_base = log10(min(d))
n_bins = np.logspace(min_base, max_base, 100)
f_mean, d_mean, binnumber = binned_statistic(d, f, statistic="mean", bins=n_bins)

# plots with fixed length bins
fig_1 = plt.figure()

plt_2 = fig_1.add_subplot(131)
degree, freq, patch = plt_2.hist(nodes_degree.values(), bins=100, alpha=0.6)

plt_2.set_title("Node Degree Histogram")
plt_2.set_xlabel("x")
plt_2.set_ylabel("P(x)")

plt_1 = fig_1.add_subplot(132)
plt_1.loglog(degree, freq[:-1], "ro")
plt_1.set_title("Loglog Degree Distribution")
plt_1.set_xlabel("x")
plt_1.set_ylabel("P(x)")

plt_3 = fig_1.add_subplot(133)
plt_3.plot(degree, freq[:-1], "go")
plt_3.set_title("Degree Distribution")
plt_3.set_xlabel("x")
plt_3.set_ylabel("P(x)")
plt.show()

# plots with log bins
fig_2 = plt.figure()

plt_2 = fig_2.add_subplot(131)
plt_2.hist(nodes_degree.values(), bins=n_bins, alpha=0.6)
plt_2.set_xscale("log")
plt_2.set_title("Node Degree Histogram")
plt_2.set_xlabel("x")
plt_2.set_ylabel("P(x)")

plt_1 = fig_2.add_subplot(132)
plt_1.loglog(d_mean[:-1], f_mean, "ro")
plt_1.set_title("Loglog Node Degree Distribution")
plt_1.set_xlabel("x")
plt_1.set_ylabel("P(x)")

plt_3 = fig_2.add_subplot(133)
plt_3.plot(d_mean[:-1], f_mean, "go")
plt_3.set_title("Degree Node Distribution")
plt_3.set_xlabel("x")
plt_3.set_ylabel("P(x)")
plt.show()

# function to estimate alpha
def estimate_alpha(xs, x_min):
    return 1 + len(xs) / sum(np.log([float(x / x_min) for x in xs]))

# estimate alphas for various x_min and plot them
x_range = xrange(1, len(d))
y = [estimate_alpha(d, x) for x in x_range]

fig_3 = plt.figure()
plt_4 = fig_3.add_subplot(111)
plt_4.plot(x_range, y)
plt_4.set_xlabel("x_min")
plt_4.set_ylabel("alpha")
plt.show()
