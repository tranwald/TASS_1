# set working directory
setwd('~/Documents/WEiTI/TASS/Projekt');

# check if needed packages are available
require("poweRlaw")
require("igraph")

# function to print data.frame
print.betweeness <- function(file_name) {
  btwns_f <- read.delim(file_name, header = TRUE, sep = "\t")
  btwns_f <- btwns_f[c(2,3)]
  colnames(btwns_f) <- c("Node", "Betweeness")
  btwns_f <- btwns_f[with(btwns_f, order(-Betweeness)), ]
  cat("Top10 betweeness centrlity for network of", length(btwns_f[,1]), "nodes:\n")
  print(btwns_f[1:10, ], row.names = FALSE)
  cat("", sep = "\n")
}
# print betweeness data.frames
print.betweeness('vec.txt')
print.betweeness('vec_half.txt')

library(poweRlaw)
# read datawith node degree's from Pajek
degrees <- read.delim("degrees_vec.txt", header = TRUE, sep = "\t", col.names = c("Id", "Node", "Degree"))[,c(2,3)]
# create a discrete power-law object
d_pl = displ$new(degrees[,2])  
# bootstrap hypothesis test to determine whether a power law distribution is plausible
bs_p = bootstrap_p(d_pl)
plot(bs_p)
hist(bs_p$bootstraps[,2], main = expression("Histogram of x"[min]), xlab =  expression("x"[min]))
hist(bs_p$bootstraps[,3], main = expression(paste("Histogram of ", hat(alpha))), xlab = expression(hat(alpha)))
# print p-value
bs_p$p # at level of 0.10 we can reject the hypothesis that data follows a power-law distribution
# estimate and set xmin
est_xmin = estimate_xmin(d_pl)
d_pl$setXmin(estimate_xmin(d_pl))
alpha_pl = estimate_pars(d_pl)
# creat log-normal object and estimate its xmin
d_ln = dislnorm$new(degrees[,2])  
#est_xmin = estimate_xmin(d_ln)
d_ln$setXmin(estimate_xmin(d_ln))
alpha_ln = estimate_pars(d_ln)
# plot both objects
plot(d_pl)
lines(d_pl, col = "red", lwd = 3)
lines(d_ln, col = "blue", lwd = 3)
legend("bottomleft", legend =  c("Log-normal Fit", "Power-law Fit"), col = c("red", "blue"), lty = c(1,1), lwd = c(3,3))

# compare duistributions
d_ln$setXmin(d_pl$getXmin())
d_ln$setPars(estimate_pars(d_ln))
comp = compare_distributions(d_pl, d_ln)

# generate vector of estimated alphas for each value in the vector of degrees
values = unique(d_pl$dat)
ests <- c()

for(v in values) {
  d_pl$setXmin(v)
  append(ests, estimate_pars(d_pl)$pars)
}

points(values, ests, type = "p")

