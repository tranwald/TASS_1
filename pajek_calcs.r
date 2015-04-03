# set working directory
setwd('~/Documents/WEiTI/TASS/Projekt');

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