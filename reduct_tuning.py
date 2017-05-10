# -*- coding: utf-8 -*-
"""
reduct_tuning.py

Created on Tue May  2 08:29:21 2017

@author: jack

找出所有属性约简的最优参数和F-measure Score
"""
from smote_svm import smote_svm

def reduct_tuning(reducts, X, y, X_scaled, nfolds):
    '''找出所有属性约简的最优参数和F-measure Score'''
    result = []
    
    for i in range(len(reducts)):
        result.append(smote_svm(reducts[i], X, y, X_scaled, nfolds))
        
    return result