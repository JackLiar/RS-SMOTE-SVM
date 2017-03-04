library(RoughSets)
##############################################################
## A.1 Example: Basic concepts of rough set theory
##############################################################
## Using hiring data set, see RoughSetData
data(RoughSetData)
decision.table <- RoughSetData$hiring.dt
## define considered attributes which are first, second, and
## third attributes
attr.P <- c(1,2,3)
## 计算不可辨别关系/compute indiscernibility relation
IND <- BC.IND.relation.RST(decision.table, feature.set = attr.P)
## 计算上下近似集/compute lower and upper approximations
roughset <- BC.LU.approximation.RST(decision.table, IND)
## 计算相关区域/Determine regions
region.RST <- BC.positive.reg.RST(decision.table, roughset)
## The decision-relative discernibility matrix and reduct
disc.mat <- BC.discernibility.mat.RST(decision.table, range.object = NULL, return.matrix = TRUE)

###############################################################
## B Example : Data analysis based on RST and FRST
## In this example, we are using wine dataset for both RST and FRST
###############################################################
## Load the data
## Not run: data(RoughSetData)
dataset <- RoughSetData$wine.dt
## Shuffle the data with set.seed
set.seed(5)
dt.Shuffled <- dataset[sample(nrow(dataset)),]
## Split the data into training and testing
idx <- round(0.8 * nrow(dt.Shuffled))
wine.tra <-SF.asDecisionTable(dt.Shuffled[1:idx,],
                              decision.attr = 14, indx.nominal = 14)
wine.tst <- SF.asDecisionTable(dt.Shuffled[
    (idx+1):nrow(dt.Shuffled), -ncol(dt.Shuffled)])
## DISCRETIZATION
cut.values <- D.discretization.RST(wine.tra,
                                   type.method = "global.discernibility")
d.tra <- SF.applyDecTable(wine.tra, cut.values)
d.tst <- SF.applyDecTable(wine.tst, cut.values)
## FEATURE SELECTION
red.rst <- FS.feature.subset.computation(d.tra,
                                         method="quickreduct.rst")
fs.tra <- SF.applyDecTable(d.tra, red.rst)
## RULE INDUCTION
rules <- RI.indiscernibilityBasedRules.RST(d.tra,
                                           red.rst)
## predicting newdata
pred.vals <- predict(rules, d.tst)
