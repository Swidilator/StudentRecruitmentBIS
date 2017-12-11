#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 14:59:19 2017

@author: kyle
"""
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


data:pd.DataFrame = pd.read_csv('Dummies.csv')


frequent_itemsets = apriori(data, min_support=0.07, use_colnames=True)

# =============================================================================
# Define Rules
# =============================================================================
rules:pd.DataFrame = association_rules(frequent_itemsets, metric = "lift", min_threshold = 1)


# =============================================================================
# Sort and output
# =============================================================================
rules.sort_values(by=['confidence'], axis=0, ascending=False, inplace=True)