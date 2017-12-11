#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:32:19 2017

@author: kyle
"""

from tensorflow.contrib import learn
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
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

feature_columns = learn.infer_real_valued_columns_from_input(x_train)

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
# apply same transformation to test data
x_test = scaler.transform(x_test)

classifier_tf = learn.DNNClassifier(feature_columns=feature_columns,
                                               hidden_units=[20, 20, 20],
                                               n_classes=2)
classifier_tf.fit(x_train, y_train, steps=5000)
predictions = list(classifier_tf.predict(x_test, as_iterable=True))
score = metrics.accuracy_score(y_test, predictions)
report = metrics.classification_report(y_test, predictions)


