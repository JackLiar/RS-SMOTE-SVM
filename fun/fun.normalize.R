fun.normalize <- function (target) {
    temp <- target
    temp <- (target - (max(target)+min(target))/2)/sqrt(max(target)^2 + min(target)^2)
    return(temp)
}