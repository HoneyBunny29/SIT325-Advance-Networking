#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: tony
"""

import pandas as pd
import numpy as np
from numpy.linalg import inv
from scipy.stats import chi2
from sklearn import preprocessing
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import math

pd.options.mode.chained_assignment = None  # default='warn'

SNR=30
NUMBER_OF_FEATURES = 3

data = pd.read_csv("datatest_task_93D_3features_100devices.csv", header=None)

def testingdevice(meandata,xtest,inv_covmat,cutoff):

    md_test_list = mahalanobis(xtest,meandata,inv_covmat)
    arr=[]
    for i in md_test_list:
        if i <= cutoff:
            arr.append(1)
        else:
            arr.append(0)

    return arr



def mahalanobis(x, meandata, inv_covmat):
    x_minus_mu = x - meandata
    left_term = np.dot(x_minus_mu, inv_covmat)
    mahal = np.dot(left_term, x_minus_mu.T)
    return mahal.diagonal()

cutoff = chi2.ppf(0.99, NUMBER_OF_FEATURES)

noise = data/(math.pow(10, (SNR/10)))
new_data = data+noise


meandata = np.mean(data)
cov = np.cov(data.T)
inv_covmat = inv(cov)


predictions = testingdevice(meandata,new_data,inv_covmat,cutoff)

y_true = np.ones(10000)


# Detection accuracy
print("Accuracy score is: ", accuracy_score(y_true, predictions)*100)
