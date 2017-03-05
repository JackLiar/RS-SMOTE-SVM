fun.switch <- function(reduct){
    result <- 1:length(reduct)
    for (i in 1:length(reduct)){
        result[i] <- switch(reduct[i],
           Clump.Thickness = 1,
           Uniformity.of.Cell.Size = 2,
           Uniformity.of.Cell.Shape = 3,
           Marginal.Adhesion = 4,
           Single.Epithelial.Cell.Size = 5,
           Bare.Nuclei = 6,
           Bland.Chromatin = 7,
           Normal.Nucleoli = 8,
           Mitoses = 9
           )
    }
    return(result)
}