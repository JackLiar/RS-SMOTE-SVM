fun.calc_rough_margin <- function(data){
    result <- rep(NA, 3)
    
    for(i in 1:(dim(data)[1]-1)){
        if(data$Client_Category[i]==1&&data$prediction[i]==0){
            result[1] <- data$`0/1`[i]
            break
        }
    }
    if(is.na(result[1])){
        for(i in 1:(dim(data)[1]-1)){
            if((data$Client_Category[i]==0&&data$prediction[i]==0)&&
               (data$prediction[i+1]==1)){
                result[1] <- data$`0/1`[i]
                break
            }
        }
    }
    for(i in (dim(data)[1]):result[1]){
        if(data$Client_Category[i]==0&&data$prediction[i]==1){
            result[2] <- data$`0/1`[i-1]
            break
        }
    }
    if(is.na(result[2])){
        for(i in 1:(dim(data)[1]-1)){
            if((data$Client_Category[i]==1&&data$prediction[i]==1)&&
               (data$prediction[i-1]==0)){
                result[2] <- data$`0/1`[i]
                break
            }
        }
    }

    return(result)
}