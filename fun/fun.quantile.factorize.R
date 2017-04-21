fun.quantile.factorize <- function(data, quantile.seq){
    len.seq <- length(quantile.seq)
    len.data <- length(data)
    data.copy <- data
    
    for(i in 1:(len.seq)){
        if(i==len.seq){
            for(j in 1:len.data)
                if(data.copy[j] == quantile.seq[i])
                    data.copy[j] <- i-1
            break
        }
        for(j in 1:len.data)
            if(data.copy[j] >= quantile.seq[i] && data.copy[j] < quantile.seq[i+1])
                data.copy[j] <- i
    }
    return(data.copy)
}