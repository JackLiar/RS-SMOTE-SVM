# 自定义分割样本函数
# df是一个data.frame
fun.partition <- function(df, strataname, proportion){
    
    library(sampling)
    class.num <- c(sum(df$Class==0),sum(df$Class==1))
    partition.table <- strata(
        df, strataname, size =c(proportion*class.num[1],
                                proportion*class.num[2]), method="srswor")
    train.id <- partition.table$ID_unit[order(partition.table$ID_unit)] # 训练集id
    df.partition.1 <- df[train.id, ]   # 训练集
    df.partition.2 <- df[-train.id, ]  # 测试集
    
    return(list(df.partition.1, df.partition.2, train.id))
    detach("package:sampling")
}