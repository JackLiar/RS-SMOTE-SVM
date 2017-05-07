setwd("D:/Documents/Code/Data_Science/Bachelor_Graduation/RS_SVM")
rm(list = ls())

# 读取数据
library(readr)
cdata <- as.data.frame(read_csv(
    "D:/Documents/Code/Data_Science/Bachelor_Graduation/RS_SVM/Credit_Data_Cleaned.csv",
    col_types = cols(Loan_Time = col_date(format = "%Y-%m-%d"), X1 = col_skip())))
detach("package:readr")

# 剔除有值为NA的记录,共计16条
cdata <- cdata[!is.na(cdata$Current_Job_Working_Years),]

# 转换成factor
cdata[,c(3:8,11,15:19)] <- sapply(cdata[,c(3:8,11,15:19)],
                                  FUN = function(x) as.integer(as.factor(x))-1)
# 将时间转换成数字
Loan_Time <- unclass(as.POSIXlt(cdata$Loan_Time))
cdata$Loan_Time_Year <- Loan_Time$year - 108
cdata$Loan_Time_Mon <- Loan_Time$mon
cdata <- cdata[,-20]
rm(Loan_Time)

# # 数据factorize
# source("./fun/fun.quantile.factorize.R")
# 
# Age.seq <- quantile(cdata$Age, seq(0,1,0.2))
# cdata$Age <- fun.quantile.factorize(cdata$Age, Age.seq)
# 
# Current_Job_Working_Years.seq <- quantile(cdata$Current_Job_Working_Years, seq(0,1,1/4))
# cdata$Current_Job_Working_Years <- fun.quantile.factorize(
#     cdata$Current_Job_Working_Years, Current_Job_Working_Years.seq)

Client_Category <- cdata$Client_Category
cdata <- cdata[,c(-1, -19)]
cdata <- cbind(cdata, Client_Category)
rm(list=ls()[ls()!="cdata"])

library(Rcpp)
library(RoughSets)
# 构造决策表
decision.table <- SF.asDecisionTable(cdata, decision.attr = 20, indx.nominal = c(1:20))

# 计算差别矩阵
disc.mat <- BC.discernibility.mat.RST(decision.table, range.object = NULL)

# 计算约简(共计20个约简)，因此无需使用遗传算法计算约简
reduct <- FS.all.reducts.computation(disc.mat)

# 使用“组合过滤”策略筛选属性子集
# 按照论文要求先计算出相关性最高和最低的两个属性，此处以和论文排序一致的pearson
# 相关系数为参考数据
cor.relation.table <- cor(cdata, method = "pearson")
combination.filtering.attributes <- colnames(
    cor.relation.table)[order(cor.relation.table[,20], decreasing = TRUE)[c(2,20)]]

save.image("./before_select.RData")

# 使用定义的函数筛选出包含相关性最高和最低两个属性的属性集
source("./fun/fun.in.R")
selected.reduct <- reduct$decision.reduct[sapply(reduct$decision.reduct, fun.in)]

# 使用自定义的函数将属性集转换成列号
source("./fun/fun.switch.R")
selected.reduct <- t(sapply(selected.reduct, fun.switch))

# 删除内存中冗余的变量
detach("package:RoughSets")
detach("package:Rcpp")


# selected.reduct[[length(selected.reduct)+1]] <- c(1,3:6,10,12,13,19)
selected.reduct[[length(selected.reduct)+1]] <- order(cor.relation.table[,20], decreasing = TRUE)[c(2:11)]
selected.reduct[[length(selected.reduct)+1]] <- c(1:19)
rm(list=ls()[ls()!="cdata"&ls()!="selected.reduct"&ls()!="reduct"])

# 将获得的约简写入 reduct.txt
if (file.exists("./reduct.txt"))
    file.remove("./reduct.txt")
sapply(selected.reduct, FUN = write,file = "./reduct.txt", append = T, sep = ",", ncolumns = 19)

library(data.table)
fwrite(cdata, "./Credit_Data.csv")