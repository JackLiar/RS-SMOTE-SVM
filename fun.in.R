## 自定义函数：判断是否是子集，并返回布尔变量
fun.in <- function(set.a, set.b = combination.filtering.attributes){
    return(all(set.b%in%set.a))
}