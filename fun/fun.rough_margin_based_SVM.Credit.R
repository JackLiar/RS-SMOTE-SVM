fun.rough_margin_based_SVM <- function(data, best){
    prediction<-best[[1]]$best.model$fitted
    train <- cbind(data[best[[2]],], prediction,
                   best[[1]]$best.model$decision.values)
    train <- train[order(-train$`0/1`, train$Client_Category),]
    rm(prediction)
    
    source("./fun/fun.calc_rough_margin.Credit.R")
    rough.margin <- fun.calc_rough_margin(train)
    
    library(Rcpp)
    library(e1071)
    test <- data[-best[[2]],]
    prediction.svm <- predict(best[[1]]$best.model, test, decision.values = T)
    prediction.rough_margin <- rep(NA, dim(test)[1])
    test <- cbind(test, prediction.svm, prediction.rough_margin,
                  attr(prediction.svm, "decision.values"))
    
    for(i in 1:dim(test)[1]){
        if(rough.margin[1] < test$`0/1`[i])
            test$prediction.rough_margin[i] <- 0
        else if(rough.margin[2] > test$`0/1`[i])
            test$prediction.rough_margin[i] <- 1
    }
    
    test <- test[order(-test$`0/1`, test$Client_Category),]
    print(table(test$Client_Category, test$prediction.svm))
    print(table(test$Client_Category, test$prediction.rough_margin, useNA = "ifany"))
    
    return(test)
}