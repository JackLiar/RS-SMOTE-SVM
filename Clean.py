# -*- coding: utf-8 -*-
"""
clean.py

Created on Sat Mar 25 19:19:05 2017

@author: jack
"""
import os
import numpy as np
import pandas as pd

os.chdir("D:\Documents\Code\Data_Science\Bachelor_Graduation\RS_SVM")

# 读取用户数据
Credit_Data=pd.read_excel('./Credit_Data.xlsx')

# 将年、月转换为月份数
def month_converter(Date):
    # print(Date[-1])
    result = 'NA'
    if pd.notnull(Date):
        if Date[-1] == '年':
            result = int(Date[0:-1])*12
        elif Date[-1] == '月':
            result = int(Date[0:-1])
        elif Date[-1] == '天':
            result = int(Date[0:-1])//30
        return result
    else:
        return 'NA'

Credit_Data.Current_Job_Working_Years = Credit_Data.Current_Job_Working_Years.apply(func=month_converter)

Credit_Data.Loan_Period = Credit_Data.Loan_Period.apply(func=month_converter)

for i in Credit_Data.index[Credit_Data.Collateral=='是']:
    Credit_Data.loc[i,'Collateral']='有'
for i in Credit_Data.index[Credit_Data.Collateral=='有 ']:
    Credit_Data.loc[i,'Collateral']='有'
for i in Credit_Data.index[Credit_Data.Collateral=='否']:
    Credit_Data.loc[i,'Collateral']='无'

for i in Credit_Data.index[Credit_Data.Other_Loan=='文件中没有']:
    Credit_Data.loc[i,'Other_Loan']='无'
for i in Credit_Data.index[Credit_Data.Other_Loan=='没有']:
    Credit_Data.loc[i,'Other_Loan']='无'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有银行车贷']:
    Credit_Data.loc[i,'Other_Loan']='车贷'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有银行购房贷款']:
    Credit_Data.loc[i,'Other_Loan']='房贷'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有信用社贷款']:
    Credit_Data.loc[i,'Other_Loan']='信用社贷款'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有购房贷款']:
    Credit_Data.loc[i,'Other_Loan']='房贷'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有银行房贷']:
    Credit_Data.loc[i,'Other_Loan']='房贷'
for i in Credit_Data.index[Credit_Data.Other_Loan=='文件中没有，估计有']:
    Credit_Data.loc[i,'Other_Loan']='估计有'
for i in Credit_Data.index[Credit_Data.Other_Loan=='文件中没有（估计有）']:
    Credit_Data.loc[i,'Other_Loan']='估计有'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有住房贷款']:
    Credit_Data.loc[i,'Other_Loan']='房贷'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有银行贷款']:
    Credit_Data.loc[i,'Other_Loan']='银行贷款'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有银行抵押贷款']:
    Credit_Data.loc[i,'Other_Loan']='银行贷款'
for i in Credit_Data.index[Credit_Data.Other_Loan=='文件中没有']:
    Credit_Data.loc[i,'Other_Loan']='无'
for i in Credit_Data.index[Credit_Data.Other_Loan=='文件中没有 ']:
    Credit_Data.loc[i,'Other_Loan']='无'
for i in Credit_Data.index[Credit_Data.Other_Loan=='文件中没']:
    Credit_Data.loc[i,'Other_Loan']='无'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有房屋贷款']:
    Credit_Data.loc[i,'Other_Loan']='房贷'
for i in Credit_Data.index[Credit_Data.Other_Loan=='有贷款']:
    Credit_Data.loc[i,'Other_Loan']='有'
for i in Credit_Data.index[Credit_Data.Other_Loan=='文件中没有找到']:
    Credit_Data.loc[i,'Other_Loan']='无'

Credit_Data.to_csv("./Credit_Data_Cleaned.csv",encoding='utf-8')
#
# for i in range(Credit_Data.shape[0]):
#     Credit_Data.Loan_Amount[i] = Credit_Data.Loan_Amount[i][0:-1]
