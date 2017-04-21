# 自定义分割样本函数
# df是一个data.frame
fun.partition <- function(df, strataname, proportion){
    
    library(sampling)
    Client_Category.num <- c(sum(df$Client_Category==0),sum(df$Client_Category==1))
    partition.table <- strata(
        df, strataname, size =c(proportion*Client_Category.num[1],
                                proportion*Client_Category.num[2]), method="srswor")
    train.id <- partition.table$ID_unit[order(partition.table$ID_unit)] # 训练集id
    df.partition.1 <- df[train.id, ]   # 训练集
    df.partition.2 <- df[-train.id, ]  # 测试集
    
    return(list(df.partition.1, df.partition.2, train.id))
    detach("package:sampling")
}