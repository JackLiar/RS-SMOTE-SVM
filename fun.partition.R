# 自定义分割样本函数
# df是一个data.frame
fun.partition <- function(df, strataname, proportion){
    
    library(sampling)
    class.num <- c(sum(df$Class==0),sum(df$Class==1))
    partition.table <- strata(
        df, strataname, size =c(proportion*class.num[1],
                                proportion*class.num[2]),method="srswor")
    df.partition.1 <- df[order(partition.table$ID_unit),]
    df.partition.2 <- df[-order(partition.table$ID_unit),]
    rownames(df.partition.1) <- c(1:dim(df.partition.1)[1])
    rownames(df.partition.2) <- c(1:dim(df.partition.2)[1])
    return(list(df.partition.1,df.partition.2))
    detach("package:sampling")
}