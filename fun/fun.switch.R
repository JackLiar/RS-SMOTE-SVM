fun.switch <- function(reduct){
    result <- 1:length(reduct)
    for (i in 1:length(reduct)){
        result[i] <- switch(reduct[i],
           Age = 1,
           Gender = 2,
           Marrige = 3,
           Education = 4,
           Bank_Credit_Condition = 5,
           Housing_Condition = 6,
           Old_Client = 7,
           Current_Job_Working_Years = 8,
           Loan_Amount = 9,
           Loan_Purpose = 10,
           Loan_Period = 11,
           Monthly_Interest_Rate = 12,
           Breach_Monthly_Interest_Rate = 13,
           Other_Loan = 14,
           Collateral = 15,
           Way_of_Mortgage = 16,        
           Full_Value = 17,
           Loan_Time_Year = 18,    
           Loan_Time_Mon = 19,
           Client_Category = 20
           )
    }
    return(result)
}