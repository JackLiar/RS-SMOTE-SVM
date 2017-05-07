# -*- coding: utf-8 -*-
"""
SVM.py

Created on Sat Mar 25 19:19:05 2017

@author: jack
"""
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re # 正则表达式模块
from sklearn.decomposition import PCA
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

## 将数据映射到二维平面以供可视化
#pca = PCA(n_components = 2)
#cdata_vis = pca.fit_transform(cdata)
#cdata_res_vis = pca.fit_transform(cdata_res)
#
## 绘制分布图
#def plot_resampling(ax, X, y, title):
#    c0 = ax.scatter(X[np.array(y == 0, dtype=bool), 0], X[np.array(y == 0, dtype=bool), 1], label="Class #0", alpha=0.5)
#    c1 = ax.scatter(X[np.array(y == 1, dtype=bool), 0], X[np.array(y == 1, dtype=bool), 1], label="Class #1", alpha=0.5)
#    ax.set_title(title)
#    ax.spines['top'].set_visible(False)
#    ax.spines['right'].set_visible(False)
#    ax.get_Xaxis().tick_bottom()
#    ax.get_yaxis().tick_left()
#    ax.spines['left'].set_position(('outward', 10))
#    ax.spines['bottom'].set_position(('outward', 10))
#    ax.set_Xlim([X[:,0].min()-10, X[:,0].max()+10])# 横轴范围
#    ax.set_ylim([X[:,1].min()-20, X[:,1].max()+20])# 纵轴范围
#
#    return c0, c1
#
#f, (ax1, ax2) = plt.subplots(2, 1)
#c0, c1 = plot_resampling(ax1, cdata_vis, cdata_class, 'Original set')
#
#plot_resampling(ax2, cdata_res_vis, cdata_class_res,'SMOTE {}'.format('svm'))
#ax1.legend((c0, c1), ('Class #0', 'Class #1'), loc=1, ncol=1, labelspacing=0.)
#
#plt.tight_layout()
#plt.show()
#f.savefig('Credit_Data_SMOTE.pdf')

# 从reduct.txt读取属性约简
Reducts = []
with open("./reduct.txt", 'r') as f:
    for line in f.readlines():
        Reducts.append(np.array(re.findall(r'\d+', line)).astype(np.int)-1)
    else:
        f.close()
        del line
#Reducts = Reducts[14:]
Reducts_len = len(Reducts)

# 加载寻找最优属性约简模块
from rs_reduct_tuning import reduct_tuning

result ,T= [] , 100
start = time.time()
for i in range(T):
    # 分割训练集数据集
    cd_train_X, cd_test_X, cd_train_y, cd_test_y = train_test_split(cdata, cdata_class, test_size=0.5)

    # 使用SMOTE算法生成样本
    cd_train_res_X, cd_train_res_y = SMOTE(kind = 'svm', ratio=1.0).fit_sample(cd_train_X, cd_train_y)
    
    # 数据标准化
    len_temp = len(cd_train_res_y)
    temp =  np.concatenate((cd_train_res_X, np.array(cd_test_X)), axis = 0)
    scaler = StandardScaler()
    temp = scaler.fit_transform(temp)

    cd_train_res_X = temp[0:len_temp]
    cd_test_X = temp[len_temp:]
    
    print(i)
    result.append(reduct_tuning(
            Reducts, cd_train_res_X, cd_train_res_y,cd_test_X, cd_test_y, 5))
end = time.time()
print("总用时为：", end - start)

precisions = []
recalls = []
f1_scores = []

for i in result:
    for j in i:
        precisions.append(j[1])
        recalls.append(j[2])
        f1_scores.append(j[3])

def reshape_mean(x):
    '''将三种指标的一维数组转换成二维数组，并计算每一行的平均值'''
    return (np.array(x).reshape(T, Reducts_len)).mean(axis=0)

def reshape_std(x):
    '''将三种指标的一维数组转换成二维数组，并计算每一行的方差'''
    return (np.array(x).reshape(T, Reducts_len)).std(axis=0)

precisions_mean, recalls_mean, f1_scores_mean = [reshape_mean(x) for x in [precisions, recalls, f1_scores]]

precisions_std, recalls_std, f1_scores_std = [reshape_std(x) for x in [precisions, recalls, f1_scores]]

def print_best_score(flag, x_name, x):
    '''输出每种指标的最大值和最大值的索引'''
    print("-" * 40)
    if flag == 0:
        print('Highest %s is: %0.5f' % (x_name, x.max()))
        print('Indexs are:', np.unique(np.array(range(len(x)))[np.array(x == x.max(), dtype = bool)]))
    elif flag ==1:
        print('Lowest %s is: %0.5f' % (x_name, x.min()))
        print('Indexs are:', np.unique(np.array(range(len(x)))[np.array(x == x.min(), dtype = bool)]))
    
for i,j in {'Mean of Precisions': precisions_mean, 'Mean of Reaclls': recalls_mean, 'Mean of F1 Scores': f1_scores_mean}.items():
    print_best_score(0,i,j)

for i,j in {'Std of Precisions': precisions_std, 'Std of Reaclls': recalls_std, 'Std of F1 Scores': f1_scores_std}.items():
    print_best_score(1,i,j)

temp = np.array([[0,0],
                 [0,0]])
for i in result:
    temp = temp + i[Reducts_len-1][4]
print(temp/T)