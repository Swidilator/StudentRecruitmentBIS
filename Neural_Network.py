#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:32:19 2017

@author: kyle
"""

import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.combine import SMOTEENN

#data:pd.DataFrame = pd.read_csv('Merged_Data_Numeric.csv')
data:pd.DataFrame = pd.read_csv('Dummies.csv')

cols = data.columns.values.tolist()
x:pd.DataFrame = normalize(
        data[cols[1:len(cols) - 1]],    # all columns except the last one
        axis=0, norm='max'              # parameters for normalization
        )


y:pd.DataFrame = data['Applicants_that_Registered']
X, x_test, Y, y_test = train_test_split(x, y, random_state=5)

sm = SMOTEENN(random_state=42)
x_train,y_train = sm.fit_sample(X,Y)

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
# apply same transformation to test data
x_test = scaler.transform(x_test)
# =============================================================================
# Descision tree : Test differet values for arguments
# =============================================================================
clf = MLPClassifier(solver='adam', alpha=0.00001, hidden_layer_sizes=(10, 5, 2), random_state=2)
clf = clf.fit(x_train, y_train)

# =============================================================================
# Test accuracy
# =============================================================================
y_pred = clf.predict(x_test)
report = classification_report(y_test, y_pred)
score = accuracy_score(y_test, y_pred)
coefficients = clf.coefs_