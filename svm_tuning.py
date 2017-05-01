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
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

# 寻找SVM最优参数和F-measure Score
def svm_tuning(X, y, nfolds):
    '''使用grid search 和 K-Fold validation 寻找最优参数'''
    Cs = [pow(10, c) for c in range(-4,1)]
    gammas = [pow(10, gamma) for gamma in range(-4,1)]
    param_grid = {'C': Cs, 'gamma' : gammas}
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    
    cv = StratifiedShuffleSplit(n_splits = nfolds, test_size = 0.5)
    grid_search = GridSearchCV(SVC(), param_grid, cv = cv)
    grid_search.fit(X_train, y_train)
    
    y_test_predict = grid_search.predict(X_test)
#    print(confusion_matrix(y_test, y_test_predict))
#    print("Precision score is: ", precision_score(y_test, y_test_predict))
#    print("F-measure score is: ", f1_score(y_test, y_test_predict))
#    print("The best parameters are %s with a score of %0.2f \n"
#          % (grid_search.best_params_, grid_search.best_score_))
    return [grid_search, precision_score(y_test, y_test_predict), recall_score(y_test, y_test_predict), f1_score(y_test, y_test_predict), confusion_matrix(y_test, y_test_predict)]