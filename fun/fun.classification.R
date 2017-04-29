fun.classification <- function(data, proportion, reduct){
    # 分层抽样
    # 加载对数据集进行分割的函数fun.partition
    source("./fun/fun.partition.R")
    ## 按比例分割
    temp<-fun.partition(data[c(reduct,10)], "Class", proportion)
    train <- as.data.frame(temp[1])
    test <- as.data.frame(temp[2])
    train.id <- temp[3][[1]]
    
    library(e1071)
    tune.result <- 
        tune(svm, Class~., data = train,
             ranges = list(gamma = 2^(seq(-15,1,by=2)), cost = 2^(seq(-5,15,by = 2))),
             tunecontrol = tune.control(sampling = "cross", cross=5),
             kernel = "radial"
             )
    # predictions <- predict(tune.result$best.model, test, decision.values = T)
    # test<-cbind(test, predictions, attr(predictions, "decision.values"))
    result <- list(tune.result, train.id)
    return(result)
}