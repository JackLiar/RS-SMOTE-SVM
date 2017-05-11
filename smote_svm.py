# -*- coding: utf-8 -*-
"""
smote_svm.py

Created on Tue May  2 08:29:21 2017

@author: jack

找出所有属性约简的最优参数和F-measure Score
"""

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn import neighbors
from svm_tuning import svm_tuning

def smote_svm(reduct, X, y, X_scaled, nfolds):
    T = [X, y]  # 训练集
    # 第一次分类预测，找出错分的少数类样本
    T_scaled_reduct = X_scaled.loc[:, reduct]
    indices, model = svm_tuning(T_scaled_reduct, T[1], T_scaled_reduct, T[1], nfolds)
    FN = [T[0].loc[indices], T[1].loc[indices]] #FN: False Positive samples
    
    # 如果少数类样本少于等于多数类样本，且有错分样本
    # 用SMOTE生成新的样本，并加入到原样本集中
    while len(FN[1])+sum(T[1]==1) <= sum(T[1]==0) and len(FN[1])!=0:
#        print([len(FN[1]), sum(T[1]==1), sum(T[1]==0)])
        
        indices_listed = list(indices)
    
        # 训练knn分类器
        knn = neighbors.KNeighborsClassifier(n_neighbors = 6)
        knn.fit(T[0][np.array(T[1]==1, dtype=bool)], T[1][np.array(T[1]==1, dtype=bool)])
    
        # 找出错分样本的k临近样本
        # 将错分样本和其k临近样本混合为新样本集合
        # 作为SMOTE生成样本的样本池
        for i in indices:
#            print('indices in the fit samples: ',knn.kneighbors([FN[0].loc[i]])[1][0])
#            print('lenght of the fit samples: ',len(T[1][np.array(T[1]==1, dtype=bool)]))
            Neighbors = T[1][np.array(
                    T[1]==1, dtype=bool)].index[knn.kneighbors([FN[0].loc[i]])[1][0]]
#            print('real indices of neighbors: ',Neighbors)
#            print('samples: ',T[1].loc[Neighbors])
            diff_set = Neighbors.difference(indices)

            for n in diff_set:
                indices_listed.append(n)
                indices = pd.Int64Index(indices_listed)
    
        FN = [T[0].loc[indices], T[1].loc[indices]]
#        print(FN[0].index)
    
        # 生成用于SMOTE的样本池
        sample_pool_X = pd.concat([T[0].loc[T[1]==0], FN[0]])
        sample_pool_y = pd.concat([T[1].loc[T[1]==0], FN[1]])
        
        length = len(sample_pool_y) # 原样本池的长度
#        print([len(FN[1]), sum(T[1]==1), sum(T[1]==0)])
        ratio = (sum(T[1]==1)+len(FN[1]))/sum(T[1]==0) # SMOTE 生成样本比例
        if ratio > 1:
            ratio = 1.0
        print('ratio: ', ratio)
        
#        print(sum(sample_pool_y==1), sum(sample_pool_y==0))
        smote = SMOTE(ratio = ratio)
        sample_pool_X, sample_pool_y = smote.fit_sample(sample_pool_X, sample_pool_y)
        print('everything is fine')
        
        new_sample_X = pd.DataFrame(sample_pool_X[length:])
        new_sample_y = pd.Series(sample_pool_y[length:])
        
        # 设置新数据的index和新数据集的columns，方便后面使用
        new_sample_X.index = pd.RangeIndex(
                len(T[1]), len(T[1])+len(new_sample_X))
        new_sample_y.index = pd.RangeIndex(
                len(T[1]), len(T[1])+len(new_sample_y))
        new_sample_X.columns = X.columns
        
        # 将新样本与原样本集混合
        T[0] = pd.concat([T[0], new_sample_X])
        T[1] = pd.concat([T[1], new_sample_y])
        
        # 新样本集标准化
        X_new_scaled = pd.DataFrame(StandardScaler().fit_transform(T[0]))
        
        # 根据属性约简筛选样本集
        X_new_scaled_reduct = X_new_scaled.loc[:, reduct]
        
        # 使用新样本集训练SVM
        indices, model = svm_tuning(
                X_new_scaled_reduct, T[1], T_scaled_reduct, y, nfolds)
        FN = [T[0].loc[indices], T[1].loc[indices]] #FN: False Positive samples
#        indices_listed = list(indices)
#    
#        # 找出错分样本的k临近样本
#        knn = neighbors.KNeighborsClassifier(n_neighbors = 6)
#        knn.fit(X_new[np.array(y_new==1, dtype=bool)], y_new[np.array(y_new==1, dtype=bool)])
#    
#        for i in indices:
#            Neighbors = pd.Int64Index(knn.kneighbors([X_new.loc[i]])[1][0])
#            Neighbors = Neighbors.difference(indices)
#
#            for n in Neighbors:
#                indices_listed.append(n)
#            indices = pd.Int64Index(indices_listed)
#        print(indices)
#        FN_X , FN_y= X_new.loc[indices], y_new.loc[indices]
#        # 生成用于SMOTE的样本池
#        sample_pool_X = pd.concat([X_new.loc[y_new==0], FN_X])
#        sample_pool_y = pd.concat([y_new.loc[y_new==0], FN_y])
        
    return model