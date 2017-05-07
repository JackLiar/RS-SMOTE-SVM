# -*- coding: utf-8 -*-
"""
Created on Sun May  7 10:47:25 2017

@author: jack
"""

from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re # 正则表达式模块
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import subprocess
import time

print(__doc__)

if os.name == 'nt':
    os.chdir("D:/Documents/Code/Data_Science/Bachelor_Graduation/RS_SVM")
else:
    os.chdir("./Code/RS_SVM")
    
# 如果没有.csv文件和.txt文件，运行R脚本生成两个文件
if not os.path.isfile('./Credit_Data.csv'):
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

# 数据标准化
scaler = StandardScaler()
cdata = scaler.fit_transform(cdata)

def svm_tuning(X, y, nfolds):
    '''使用grid search 和 K-Fold validation 寻找最优参数'''
    Cs = [pow(10, c) for c in range(-4,1)]
    gammas = [pow(10, gamma) for gamma in range(-4,1)]
    param_grid = {'C': Cs, 'gamma' : gammas}
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    
    cv = StratifiedShuffleSplit(n_splits = nfolds, test_size = 0.5)
    grid_search = GridSearchCV(SVC(), param_grid, cv = cv)
    grid_search.fit(X_train, y_train)
    
    test_y_predict = grid_search.predict(X_test)
#    print(confusion_matrix(y_test, y_test_predict))
#    print("Precision score is: ", precision_score(y_test, y_test_predict))
#    print("F-measure score is: ", f1_score(y_test, y_test_predict))
#    print("The best parameters are %s with a score of %0.2f \n"
#          % (grid_search.best_params_, grid_search.best_score_))
    return [grid_search, precision_score(y_test, test_y_predict), recall_score(y_test, test_y_predict), f1_score(y_test, test_y_predict), confusion_matrix(y_test, test_y_predict)]

result ,T= [] , 100
start = time.time()
for i in range(T):
    print(i)
    result.append(svm_tuning(cdata, cdata_class, 5))
end = time.time()
print("总用时为：", end - start)

precisions = []
recalls = []
f1_scores = []

for i in result:
        precisions.append(i[1])
        recalls.append(i[2])
        f1_scores.append(i[3])
        
print("Mean of precisions:", np.mean(precisions))
print("Mean of recalls:", np.mean(recalls))
print("Mean of f1_scores:", np.mean(f1_scores))