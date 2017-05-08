# -*- coding: utf-8 -*-
"""
svm_tuning.py

Created on Tue May  2 08:27:22 2017

@author: jack

使用grid search 和 K-Fold validation 寻找最优参数
"""
# import necessary modules for grid search & cross-validation & SVM
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import time

# 寻找SVM最优参数和F-measure Score
def svm_tuning(train_X, train_y, test_X, test_y, nfolds):
    '''使用grid search 和 K-Fold validation 寻找最优参数'''
    start = time.time()
    Cs = [pow(2, c) for c in range(-4,5)]
    gammas = [pow(2, gamma) for gamma in range(-4,0)]
    param_grid = {'C': Cs, 'gamma' : gammas}
    
    cv = StratifiedShuffleSplit(n_splits = nfolds, test_size = 0.5)
    grid_search = GridSearchCV(SVC(), param_grid, cv = cv)
    grid_search.fit(train_X, train_y)
    
    test_y_predict = grid_search.predict(test_X)
    end = time.time()
    Time = end-start
#    print(confusion_matrix(y_test, y_test_predict))
#    print("Precision score is: ", precision_score(y_test, y_test_predict))
#    print("F-measure score is: ", f1_score(y_test, y_test_predict))
#    print("The best parameters are %s with a score of %0.2f \n"
#          % (grid_search.best_params_, grid_search.best_score_))
    return [Time, precision_score(test_y, test_y_predict), recall_score(test_y, test_y_predict), f1_score(test_y, test_y_predict), confusion_matrix(test_y, test_y_predict)]