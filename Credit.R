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
save.image("./original.RData")

# 转换成factor
cdata[,c(3:8,11,15:19)] <- sapply(cdata[,c(3:8,11,15:19)],
                                  FUN = function(x) as.integer(as.factor(x)))
# 年龄与贷款目的马赛克图
# 可以看出，主要目的是用于经营
# age_purpose <- table(cdata$Age,cdata$Loan_Purpose)
# mosaicplot(age_purpose)

# 将时间转换成数字
Loan_Time <- unclass(as.POSIXlt(cdata$Loan_Time))
cdata$Loan_Time_Year <- Loan_Time$year - 108
cdata$Loan_Time_Mon <- Loan_Time$mon
cdata <- cdata[,-20]
rm(Loan_Time)

# 数据factorize
source("./fun/fun.quantile.factorize.R")

Age.seq <- quantile(cdata$Age, seq(0,1,0.2))
cdata$Age <- fun.quantile.factorize(cdata$Age, Age.seq)

Current_Job_Working_Years.seq <- quantile(cdata$Current_Job_Working_Years, seq(0,1,1/4))
cdata$Current_Job_Working_Years <- fun.quantile.factorize(
    cdata$Current_Job_Working_Years, Current_Job_Working_Years.seq)

Loan_Amount.seq <- quantile(cdata$Loan_Amount, seq(0,1,1/4))
cdata$Loan_Amount <- fun.quantile.factorize(cdata$Loan_Amount,Loan_Amount.seq)

# Loan_Period.seq <- c(1,6,10,12)
Loan_Period.seq <- c(1,3,4,6,7,11,12)
cdata$Loan_Period <- fun.quantile.factorize(cdata$Loan_Period,Loan_Period.seq)

Monthly_Interest_Rate.seq <- c(0.0117,0.0129,0.0128,0.01323,0.015,0.0151,0.0153)
# Monthly_Interest_Rate.seq <- c(0.0117,0.0135,0.0138,0.015,0.0153)
cdata$Monthly_Interest_Rate <- fun.quantile.factorize(cdata$Monthly_Interest_Rate,
                                            Monthly_Interest_Rate.seq)

# Breach_Monthly_Interest_Rate.seq <- c(0.01521,0.01677,0.01719,0.0195,0.0196,0.01989)
Breach_Monthly_Interest_Rate.seq <- c(0.01521,0.01755,0.0179,0.0195,0.01989)
cdata$Breach_Monthly_Interest_Rate <- fun.quantile.factorize(cdata$Breach_Monthly_Interest_Rate,
                                                      Breach_Monthly_Interest_Rate.seq)
rm(list=ls()[ls()!="cdata"])
ID <- cdata$ID
Client_Category <- cdata$Client_Category
cdata <- cdata[,c(-1,-19)]
cdata <- cbind(cdata, Client_Category)


# temp <- cbind(cdata$Loan_Period,
#               fun.quantile.factorize(cdata$Loan_Period,
#                                      Loan_Period.seq))
# temp <- temp[order(temp[,1]),]
# table(temp[,2])

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

# 使用定义的函数筛选出包含相关性最高和最低两个属性的属性集
source("./fun/fun.in.R")
selected.reduct <- reduct$decision.reduct[sapply(reduct$decision.reduct, fun.in)]

# 使用自定义的函数将属性集转换成列号
source("./fun/fun.switch.Credit.R")
selected.reduct <- t(sapply(selected.reduct, fun.switch))

# 删除内存中冗余的变量
detach("package:RoughSets")
detach("package:Rcpp")
rm(list=ls()[ls()!="cdata"&ls()!="selected.reduct"])
selected.reduct[[length(selected.reduct)+1]] <- c(1:19)

# 数据归一化处理
# 此处不知原文使用何种方法标准化到[-1,1]区间，故使用数据-中位数/最大最小平方和的
# 方式进行归一化
source("./fun/fun.normalize.R")
temp <- as.list(cdata[,-20])
cdata[,-20]<-as.data.frame(lapply(temp, fun.normalize))

# 删除内存中冗余的变量
rm("temp","fun.normalize")
save.image("./before_classification.RData")

# 分类计算
source("./fun/fun.classification.R")
library(foreach)
library(doParallel)
cl <- makeCluster(3)
registerDoParallel(cl)
rm(cl)

# 输入分层抽样比例，对Class属性因子化处理
proportion <- c(0.8, 0.7, 0.5)
cdata$Client_Category <- factor(cdata$Client_Category, levels=c(1, 2), labels=c(0, 1))
# 循环次数
n <- 1

system.time(result<-foreach(t = 1:n) %do% {
    foreach(i = 1:length(proportion)) %do% {
        foreach(j = 1:length(selected.reduct)) %dopar% {
            fun.classification(cdata, proportion[i], selected.reduct[[j]])}
        }
    }
)
save.image("./result.RData")

# 找出性能最好的一次计算结果
source("./fun/fun.find_best_parameters.Credit.R")
(best.iter<-fun.find_best_parameters(result,c(n,length(proportion),length(selected.reduct))))
best.result <- result[[best.iter[1]]][[best.iter[2]]][[best.iter[3]]]

# Rough Margin Based SVM
source("./fun/fun.rough_margin_based_SVM.Credit.R")
test <- fun.rough_margin_based_SVM(cdata[, c(selected.reduct[[best.iter[3]]], 20)],
                                   best.result)


Table <- table(test$Client_Category, test$prediction.svm)

TP <- Table[4]
TN <- Table[1]
FP <- Table[3]
FN <- Table[2]

TPR <- TP/(TP+FN)
TNR <- TN/(TN+FP)
precision <- TP/(FP+TP)
(G_mean <- sqrt(TPR*TNR))
(F_measure <- 2*TPR*precision/(TPR+precision))

