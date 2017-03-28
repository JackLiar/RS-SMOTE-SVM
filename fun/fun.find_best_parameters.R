fun.find_best_parameters <- function(result, iters){
    best.iter<-c(0,0,0)
    best<-result[[1]][[1]][[1]][[1]]$best.performance
    
    for(i in 1:iters[1]){
        for (j in 1:iters[2]){
            for(k in 1:iters[3]){
                if(best > result[[i]][[j]][[k]][[1]]$best.performance){
                    best <- result[[i]][[j]][[k]][[1]]$best.performance
                    best.iter<-c(i,j,k)
                }
            }
        }
    }
    
    return(best.iter)
}