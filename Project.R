setwd("D:/Documents/Code/R/RoughSetStudy")
rm(list = ls())

# 读取数据
library(readr)
bcdata <- read_csv("./breast-cancer-wisconsin.csv", 
                   col_types = cols(`Bare Nuclei` = col_integer(), 
                                    ID = col_skip()))
detach("package:readr")

# 剔除有值为NA的记录,共计16条
bcdata <- bcdata[!is.na(bcdata$`Bare Nuclei`),]

# 2,4转换为0,1
bcdata$Class[bcdata$Class == 2] <- 0
bcdata$Class[bcdata$Class == 4] <- 1
# 矩阵化数据
#bcdata_m<-as.matrix(bcdata)

library(Rcpp)
library(RoughSets)
#library(RoughSetKnowledgeReduction)

# 构造决策表
decision.table <- SF.asDecisionTable(dataset = bcdata, decision.attr = 10, indx.nominal = c(1:10))
colnames(decision.table) <- colnames(bcdata)

# 计算差别矩阵
disc.mat <- BC.discernibility.mat.RST(decision.table, range.object = NULL)

# 计算约简(共计20个约简)，因此无需使用遗传算法计算约简
reduct <- FS.all.reducts.computation(disc.mat)

# 计算协方差矩阵，并以三种不同的相关系数计算相关系数
bcdata.cov <- cov(bcdata)
# 相关性降序排列：Bare Nuclei，Uniformity of Cell Size，Uniformity of Cell Shape

cor.relation.table <- cor(bcdata, method = "pearson")
# 相关性降序排列：Bare Nuclei，Uniformity of Cell Shape，Uniformity of Cell Size

cor.relation.table <- cor(bcdata, method = "spearman")
# 相关性降序排列：Uniformity of Cell Size，Uniformity of Cell Shape，Bare Nuclei

cor.relation.table <- cor(bcdata, method = "kendall")
# 相关性降序排列：Bare Nuclei，Uniformity of Cell Size，Uniformity of Cell Shape

# 使用“组合过滤”策略筛选属性子集
# 按照论文要求先计算出相关性最高和最低的两个属性，此处以和论文排序一致的pearson
# 相关系数为参考数据
cor.relation.table <- cor(bcdata, method = "pearson")
combination.filtering.attributes <- colnames(
    cor.relation.table)[order(cor.relation.table[,10], decreasing = TRUE)
                        [c(2,10)]]

reduct$decision.reduct

## 自定义函数：判断是否是子集，并返回布尔变量
fun.in <- function(set.a, set.b = combination.filtering.attributes){
    return(all(set.b%in%set.a))
}
# 使用定义的函数筛选出包含相关性最高和最低两个属性的属性集
selected.reduct <- reduct$decision.reduct[sapply(reduct$decision.reduct, fun.in)]
# 删除内存中冗余的变量
rm(list=ls()[c(-1,-length(ls()))])

library(e1071)
