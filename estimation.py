import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from math import log10
from scipy.stats import binned_statistic
import operator

from os import listdir
files = listdir('.')

# load graph from file
with open("coa_matrix.net") as filename:
    G = nx.read_pajek(filename)

# get nodes degrees and degree frequencies
nodes_degree = G.degree()
cd = sorted([(k,v) for k,v in Counter(nodes_degree.values()).iteritems()], key=operator.itemgetter(1))
d, f = list(zip(*cd))
#d = map(float, d)
#f = [x/float(sum(f)) for x in f]

# calculate log bins
max_base = max(log10(max(d)), log10(max(f)))
min_base = log10(min(d))
n_bins = np.logspace(min_base, max_base, 100)
f_mean, d_mean, binnumber = binned_statistic(d, f, statistic="mean", bins=n_bins)

# plots with fixed length bins
fig_1 = plt.figure()

plt_2 = fig_1.add_subplot(131)
degree, freq, patch = plt_2.hist(sorted(nodes_degree.values()), bins=100, alpha=0.6)

plt_2.set_title("Node Degree Histogram")
plt_2.set_xlabel("x")
plt_2.set_ylabel("P(x)")

plt_1 = fig_1.add_subplot(132)
plt_1.loglog(freq[:-1], degree, "ro")
plt_1.set_title("Loglog Degree Distribution")
plt_1.set_xlabel("x")
plt_1.set_ylabel("P(x)")

plt_3 = fig_1.add_subplot(133)
plt_3.plot(freq[:-1], degree, "go")
plt_3.set_title("Degree Distribution")
plt_3.set_xlabel("x")
plt_3.set_ylabel("P(x)")
# plt.show()

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
# plt.show()

# function to estimate alpha
def estimate_alpha(xs, x_min):
    from numpy import log, sum
    xs_cutoff = [x / (x_min - 0.5) for x in xs if x >= x_min]
    return 1 + len(xs_cutoff) / sum(log(xs_cutoff))

# estimate alphas for various x_min and plot them
x_range = xrange(1, len(d))
y = [estimate_alpha(d, x) for x in x_range]

fig_3 = plt.figure()
plt_4 = fig_3.add_subplot(111)
plt_4.plot(x_range, y)
plt_4.set_xlabel("x_min")
plt_4.set_ylabel("alpha")
plt.show()

# estimate alpha for point cpicked from the plot
print "For x_min = %d, alpha = %f" % (104, estimate_alpha(d, 104))

#calculate x_min and alpha using powerlaw module
import powerlaw
results = powerlaw.Fit(d)
print "powerlaw module: x_min = %d, alpha = %f" % (results.power_law.xmin, results.power_law.alpha)

# R, p = results.distribution_compare('power_law', 'lognormal')
# print R
# print p
