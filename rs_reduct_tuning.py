# -*- coding: utf-8 -*-
"""
reduct_tuning.py

Created on Tue May  2 08:29:21 2017

@author: jack

找出所有属性约简的最优参数和F-measure Score
"""
from rs_svm_tuning import svm_tuning

def reduct_tuning(reducts, train_X, train_y, test_X, test_y, nfolds):
    '''找出所有属性约简的最优参数和F-measure Score'''
    grid_result = []
    
    for i in range(len(reducts)):
        grid_result.append(svm_tuning(train_X.loc[:, reducts[i]], train_y, test_X.loc[:, reducts[i]], test_y, nfolds))
        
    return grid_result