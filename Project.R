setwd("D:/Documents/Code/R/RoughSetStudy")
rm(list = ls())

# 读取数据
library(readr)
bcdata <- as.data.frame(read_csv("./breast-cancer-wisconsin.csv", 
                   col_types = cols(`Bare Nuclei` = col_integer(),ID = col_skip())))
detach("package:readr")

# 剔除有值为NA的记录,共计16条
bcdata <- bcdata[!is.na(bcdata$`Bare Nuclei`),]
names(bcdata) <- c("Clump.Thickness", "Uniformity.of.Cell.Size", "Uniformity.of.Cell.Shape",
                  "Marginal.Adhesion", "Single.Epithelial.Cell.Size", "Bare.Nuclei",
                  "Bland.Chromatin", "Normal.Nucleoli", "Mitoses", "Class")

# 2,4转换为0,1
bcdata$Class[bcdata$Class == 2] <- 0
bcdata$Class[bcdata$Class == 4] <- 1

library(Rcpp)
library(RoughSets)

# 构造决策表
decision.table <- SF.asDecisionTable(dataset = bcdata, decision.attr = 10, indx.nominal = c(1:10))

# 计算差别矩阵
disc.mat <- BC.discernibility.mat.RST(decision.table, range.object = NULL)

# 计算约简(共计20个约简)，因此无需使用遗传算法计算约简
reduct <- FS.all.reducts.computation(disc.mat)

# 使用“组合过滤”策略筛选属性子集
# 按照论文要求先计算出相关性最高和最低的两个属性，此处以和论文排序一致的pearson
# 相关系数为参考数据
cor.relation.table <- cor(bcdata, method = "pearson")
combination.filtering.attributes <- colnames(
    cor.relation.table)[order(cor.relation.table[,10], decreasing = TRUE)[c(2,10)]]

# 使用定义的函数筛选出包含相关性最高和最低两个属性的属性集
source("./fun.in.R")
selected.reduct <- reduct$decision.reduct[sapply(reduct$decision.reduct, fun.in)]

# 删除内存中冗余的变量
detach("package:RoughSets")
detach("package:Rcpp")
rm(list=ls()[c(-1,-length(ls()))])


# 数据归一化处理
# 此处不知原文使用何种方法标准化到[-1,1]区间，故使用数据-中位数/最大最小平方和的
# 方式进行归一化
source("./fun.normalize.R")
temp <- as.list(bcdata[,-10])
bcdata[,-10]<-as.data.frame(lapply(temp, fun.normalize))

# 删除内存中冗余的变量
rm("temp","fun.normalize")

# 分类计算
source("./fun.classification.R")
library(foreach)
library(doParallel)
cl <- makeCluster(3)
registerDoParallel(cl)

# 输入分层抽样比例，对Class属性因子化处理
proportion <- c(0.8, 0.7, 0.5)
bcdata$Class <- factor(bcdata$Class, levels=c(0, 1), labels=c(0, 1))

system.time(result<-foreach(i = 1:3) %do% {
    r <- foreach(j = 1:length(proportion)) %dopar% {
        fun.classification(proportion[j])
    }
})