# -*- coding: utf-8 -*-
"""
RS-SMOTE-SVM.py

Created on Sat Mar 25 19:19:05 2017

@author: jack
"""

import numpy as np
import os
import pandas as pd
import re # 正则表达式模块
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import subprocess
import time

print(__doc__)

if os.name == 'nt':
    os.chdir("D:/Documents/Code/Data_Science/Bachelor_Graduation/RS_SVM")
else:
    os.chdir("./Code/RS_SVM")
# 如果没有.csv文件和.txt文件，运行R脚本生成两个文件
if not (os.path.isfile('./Credit_Data.csv') and os.path.isfile('./reduct.txt')):
    if os.name == 'nt':
        subprocess.call(['C:/Program Files/R/R-3.4.0/bin/Rscript', '--vanilla', './Calculate_Reduct.R'], shell = True)
    else:
        subprocess.call(['/usr/lib/R/bin/Rscript', '--vanilla', './Calculate_Reduct.R'], shell = True)

# 从.csv文件读取数据，并将基本数据和Class分开
cdata = pd.read_csv("./Credit_Data.csv")
cdata_class = cdata.Client_Category
cdata = cdata[cdata.columns[0:19]]
cdata['Loan_Amount'] = cdata['Loan_Amount']/10000
cdata[['Monthly_Interest_Rate','Breach_Monthly_Interest_Rate']] = cdata[['Monthly_Interest_Rate','Breach_Monthly_Interest_Rate']]*100

cdata_scaled = pd.DataFrame(StandardScaler().fit_transform(cdata))

# 从reduct.txt读取属性约简
Reducts = []
with open("./reduct.txt", 'r') as f:
    for line in f.readlines():
        Reducts.append(np.array(re.findall(r'\d+', line)).astype(np.int)-1)
    else:
        f.close()
        del line
#Reducts = Reducts[15:]
Reducts_len = len(Reducts)

# 加载寻找最优属性约简模块
from reduct_tuning import reduct_tuning

result ,T= [] , 10
start = time.time()
for i in range(T):
    # 分割训练集数据集
    cd_train_X, cd_test_X, cd_train_y, cd_test_y = train_test_split(cdata, cdata_class, test_size=0.5)
    while sum(cd_train_y) <= 6 or sum(cd_train_y) >= 17:
        cd_train_X, cd_test_X, cd_train_y, cd_test_y = train_test_split(cdata, cdata_class, test_size=0.5)
    
    print(i+1)
    result.append(reduct_tuning(Reducts, cdata, cdata_class, cdata_scaled, 5))
end = time.time()
print("总用时为：", end - start)

#Time = []
#precisions = []
#recalls = []
#f1_scores = []
#
#for i in result:
#    for j in i:
#        Time.append(j[0])
#        precisions.append(j[1])
#        recalls.append(j[2])
#        f1_scores.append(j[3])
#
#def reshape_mean(x):
#    '''将三种指标的一维数组转换成二维数组，并计算每一行的平均值'''
#    return (np.array(x).reshape(T, Reducts_len)).mean(axis=0)
#
#def reshape_std(x):
#    '''将三种指标的一维数组转换成二维数组，并计算每一行的方差'''
#    return (np.array(x).reshape(T, Reducts_len)).std(axis=0)
#
#def reshape_sum(x):
#    '''将三种指标的一维数组转换成二维数组，并计算每一行的方差'''
#    return (np.array(x).reshape(T, Reducts_len)).sum(axis=0)
#
#precisions_mean, recalls_mean, f1_scores_mean = [reshape_mean(x) for x in [precisions, recalls, f1_scores]]
#
#precisions_std, recalls_std, f1_scores_std = [reshape_std(x) for x in [precisions, recalls, f1_scores]]
#
#Time_sum = reshape_sum(Time)
#
#def print_best_score(flag, x_name, x):
#    '''输出每种指标的最大值和最大值的索引'''
#    print("-" * 40)
#    if flag == 0:
#        print('Highest %s is: %0.5f' % (x_name, x.max()))
#        print('Indexs are:', np.unique(np.array(range(len(x)))[np.array(x == x.max(), dtype = bool)]))
#    elif flag ==1:
#        print('Lowest %s is: %0.5f' % (x_name, x.min()))
#        print('Indexs are:', np.unique(np.array(range(len(x)))[np.array(x == x.min(), dtype = bool)]))
#    
#for i,j in {'Mean of Precisions': precisions_mean, 'Mean of Reaclls': recalls_mean, 'Mean of F1 Scores': f1_scores_mean}.items():
#    print_best_score(0,i,j)
#
#for i,j in {'Std of Precisions': precisions_std, 'Std of Reaclls': recalls_std, 'Std of F1 Scores': f1_scores_std}.items():
#    print_best_score(1,i,j)
#
#temp = np.array([[0,0],
#                 [0,0]])
#for i in result:
#    temp = temp + i[30][4]
#print(temp/T)