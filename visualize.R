setwd("D:/Documents/Code/Data_Science/Bachelor_Graduation/RS_SVM")
rm(list = ls())
load("./before_select.RData")

library(ggplot2)
library(reshape2)
library(showtext)
library(Cairo)
showtext.auto()


colnames(cor.relation.table) <- c(1:20)
row.names(cor.relation.table) <- c(1:20)
cormat <- cor.relation.table

# Get lower triangle of the correlation matrix
get_lower_tri<-function(cormat){
    cormat[upper.tri(cormat)] <- NA
    return(cormat)
}

# reorder_cormat <- function(cormat){
#     # Use correlation between variables as distance
#     dd <- as.dist((1-cormat)/2)
#     hc <- hclust(dd)
#     cormat <-cormat[hc$order, hc$order]
# }
# 
# cormat <- reorder_cormat(cor.relation.table)
lower_tri <- get_lower_tri(cormat)
melted_cor <- melt(lower_tri, na.rm = T)

cairo_pdf("D:/Documents/毕业设计/Paper/figures/correlation.pdf")
ggplot(data = melted_cor, aes(x=Var1, y=Var2, fill=value)) + 
    geom_tile(color = "white")+
    scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                         midpoint = 0, limit = c(-1,1), space = "Lab", 
                         name="Pearson\nCorrelation")+
    theme_minimal()+ 
    theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                     size = 12, hjust = 1))+
    coord_fixed()
dev.off()
