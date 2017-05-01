# -*- coding: utf-8 -*-
"""
reduct_tuning.py

Created on Tue May  2 08:29:21 2017

@author: jack

找出所有属性约简的最优参数和F-measure Score
"""
from svm_tuning import svm_tuning

def reduct_tuning(reducts, X, y, nfolds):
    '''找出所有属性约简的最优参数和F-measure Score'''
    grid_result = []
    
    for i in range(len(reducts)):
        grid_result.append(svm_tuning(X[:, reducts[i]], y, nfolds))
        
    return grid_result