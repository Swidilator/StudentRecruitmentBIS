#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:53:02 2017

@author: kyle
"""

import pandas as pd
from sklearn import tree
from sklearn.preprocessing import normalize
from sklearn.metrics import accuracy_score, classification_report

from sklearn.model_selection import train_test_split

# =============================================================================
# import data
# =============================================================================
data:pd.DataFrame = pd.read_csv('Merged_Data_Numeric.csv')
#data:pd.DataFrame = pd.read_csv('Dummies.csv')



# data.drop('Student_Number', axis = 1, inplace=True)

cols = data.columns.values.tolist()
x:pd.DataFrame= data[cols[1:len(cols) - 1]]    # all columns except the last one
y:pd.DataFrame = data['Applicants_that_Registered']
x_train, x_test, y_train, y_test = train_test_split(x,y, random_state=5)

# =============================================================================
# Descision tree : Test differet values for arguments
# =============================================================================
clf = tree.DecisionTreeClassifier(criterion='entropy', random_state=5, max_depth=8, min_samples_leaf=12)
clf = clf.fit(x_train, y_train)

# =============================================================================
# Test accuracy
# =============================================================================
y_pred = clf.predict(x_test)
score = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
