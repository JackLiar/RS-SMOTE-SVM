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
    X_new, y_new = X, y
    # 第一次分类预测，找出错分的少数类样本
    X_scaled_reduct = X_scaled.loc[:, reduct]
    indices, model = svm_tuning(X_scaled_reduct, y_new, X_scaled_reduct, y_new, nfolds)
    indices_listed = list(indices)
    
    # 找出错分样本的k临近样本
    knn = neighbors.KNeighborsClassifier(n_neighbors = 6)
    knn.fit(X_new[np.array(y_new==1, dtype=bool)], y_new[np.array(y_new==1, dtype=bool)])
    
    for i in indices:
        Neighbors = pd.Int64Index(knn.kneighbors([X_new.loc[i]])[1][0])
        diff_set = Neighbors.difference(indices)

        for n in diff_set:
            indices_listed.append(n)
        indices = pd.Int64Index(indices_listed)
    
    FN_X , FN_y= X_new.loc[indices], y_new.loc[indices]
    
    # 生成用于SMOTE的样本池
    sample_pool_X = pd.concat([X_new.loc[y==0], FN_X])
    sample_pool_y = pd.concat([y_new.loc[y==0], FN_y])
    
    # 如果少数类样本少于等于多数类样本，且有错分样本
    # 用SMOTE生成新的样本，并加入到原样本集中
    while len(FN_y)+sum(y_new==1) <= sum(y_new==0) and len(FN_y)!=0:
        print([len(FN_y), sum(y_new==1), sum(y_new==0)])
        
        ratio = (sum(y_new==1)+len(FN_y))/sum(y_new==0) # SMOTE 生成样本比例
        if ratio > 1:
            ratio = 1
        length = len(sample_pool_y) # 原样本池的长度
        
        print(sum(sample_pool_y==1), sum(sample_pool_y==0))
        smote = SMOTE(ratio = ratio)
        sample_pool_X, sample_pool_y = smote.fit_sample(sample_pool_X, sample_pool_y)
        
        new_sample_X = pd.DataFrame(sample_pool_X[length:])
        new_sample_y = pd.Series(sample_pool_y[length:])
        
        # 设置新数据的index和新数据集的columns，方便后面使用
        new_sample_X.index = pd.RangeIndex(
                len(y_new), len(y_new)+len(new_sample_X))
        new_sample_y.index = pd.RangeIndex(
                len(y_new), len(y_new)+len(new_sample_y))
        new_sample_X.columns = X.columns
        
        # 将新样本与原样本集混合
        X_new = pd.concat([X_new, new_sample_X])
        y_new = pd.concat([y_new, new_sample_y])
        
        # 新样本集标准化
        X_new_scaled = pd.DataFrame(StandardScaler().fit_transform(X_new))
        
        # 根据属性约简筛选样本集
        X_new_scaled_reduct = X_new_scaled.loc[:, reduct]
        
        # 使用新样本集训练SVM
        indices, model = svm_tuning(
                X_new_scaled_reduct, y_new, X_scaled_reduct, y, nfolds)
        indices_listed = list(indices)
    
        # 找出错分样本的k临近样本
        knn = neighbors.KNeighborsClassifier(n_neighbors = 6)
        knn.fit(X_new[np.array(y_new==1, dtype=bool)], y_new[np.array(y_new==1, dtype=bool)])
    
        for i in indices:
            Neighbors = pd.Int64Index(knn.kneighbors([X_new.loc[i]])[1][0])
            Neighbors = Neighbors.difference(indices)

            for n in Neighbors:
                indices_listed.append(n)
            indices = pd.Int64Index(indices_listed)
        print(indices)
        FN_X , FN_y= X_new.loc[indices], y_new.loc[indices]
        # 生成用于SMOTE的样本池
        sample_pool_X = pd.concat([X_new.loc[y_new==0], FN_X])
        sample_pool_y = pd.concat([y_new.loc[y_new==0], FN_y])
        
    return model