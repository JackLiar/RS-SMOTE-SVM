fun.classification <- function(proportion, reduct){
    # 分层抽样
    # 加载对数据集进行分割的函数fun.partition
    source("./fun/fun.partition.R")
    ## 按比例 分割
    temp<-fun.partition(bcdata[c(reduct,10)], "Class", proportion)
    train <- as.data.frame(temp[1])
    test <- as.data.frame(temp[2])
    
    library(e1071)
    tune.result <- tune(svm, Class~., data = train,
                              ranges = list(gamma = 2^(seq(-15,1,by=2)), cost = 2^(seq(-5,15,by = 2))),
                              tunecontrol = tune.control(sampling = "cross", cross=5),
                              kernel = "polynomial"
    )
    predictions <- predict(tune.result$best.model, test, decision.values = T)
    result <- list(tune.result, predictions)
    # table(predictions, bcdata.partition.20$Class)
    return(result)
}