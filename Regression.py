#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:43:30 2017

@author: kyle
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler
from imblearn.combine import SMOTEENN

from sklearn.metrics import accuracy_score, classification_report


data:pd.DataFrame = pd.read_csv('Merged_Data_Numeric.csv')
# data:pd.DataFrame = pd.read_csv('Dummies.csv')


cols = data.columns.values.tolist()
x:pd.DataFrame = data[cols[2:len(cols) - 1]]
y:pd.DataFrame = data['Applicants_that_Registered']


X, x_test, Y, y_test = train_test_split(x, y, random_state=5)

sm = SMOTEENN(random_state=42)
x_train,y_train = sm.fit_sample(X,Y)

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
# apply same transformation to test data
x_test = scaler.transform(x_test)



linreg = LinearRegression()
linreg.fit(x_train, y_train)
y_pred = linreg.predict(x_test)
score = linreg.score(x_test, y_test)