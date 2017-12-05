# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def change_greater_than_zero_to_one(x):
    if x > 0:
        return 1
    else:
        return 0
    
def change_zero_to_negative_one(x):
    if x == 0:
        x = -1
        
def change_UNKNOWN_to_negative_one(x):
    if x == 'UNKNOWN':
        x = -1
        
def financial_application_sort_outcome(x):
    if x == 'Student Offered the Award':
        return 1
    else:
        return 0
    
def residential_application_sort_outcome(x):
    if x == 'Firm res offer':
        return 1
    else:
        return 0

# =============================================================================
# Read in files
# =============================================================================
application_data = pd.DataFrame = pd.read_csv('Admission Application Data.csv')
funding_data = pd.DataFrame = pd.read_csv('Vac Work Information Financial.csv')
residence_data = pd.DataFrame = pd.read_csv('Vac Work Information Residential.csv')

# =============================================================================
# Rename all columns to remove spaces
# =============================================================================
application_data= application_data.rename(columns=lambda x: x.strip().replace(' ','_'))
funding_data = funding_data.rename(columns=lambda x: x.strip().replace(' ','_'))
residence_data = residence_data.rename(columns=lambda x: x.strip().replace(' ','_'))
#cost_data = cost_data.rename(columns=lambda x: x.strip().replace(' ','_'))


a = residence_data['Res_Appl_Status_Description'].value_counts()
# b = cost_data['Item_type_descr'].value_counts()
c = application_data['Matric_Province'].value_counts()


# =============================================================================
# Drop and Transfrom from other tables
# =============================================================================
funding_data['Application_Status_Description'] = funding_data['Application_Status_Description'].map(lambda x: financial_application_sort_outcome(x))
funding_data.sort_values(by=['Student_Number','Application_Calendar_Year','Application_Status_Description'], ascending = False, inplace=True)
funding_data.drop('Application_Status', axis=1, inplace = True)
funding_data.drop('Funding_Level', axis=1, inplace = True)
funding_data.drop_duplicates(keep='first',subset=['Student_Number', 'Application_Calendar_Year'], inplace = True)

residence_data.drop('Res_Application_Status', axis=1, inplace = True)
residence_data['Res_Appl_Status_Description'] = residence_data['Res_Appl_Status_Description'].map(lambda x: residential_application_sort_outcome(x))
residence_data.sort_values(by=['Student_Number', 'Calendar_Instance_Year', 'Res_Appl_Status_Description'], ascending = False, inplace = True)
residence_data.drop_duplicates(keep='first',subset=['Student_Number', 'Calendar_Instance_Year'], inplace = True)



# =============================================================================
# Joins
# =============================================================================
join1 = application_data.merge(funding_data, left_on=['Student_Number', 'Calendar_Inst_Year'], right_on=['Student_Number', 'Application_Calendar_Year'], how='left')
join2 = pd.DataFrame = join1.merge(residence_data, left_on=['Student_Number', 'Calendar_Inst_Year'], right_on=['Student_Number', 'Calendar_Instance_Year'], how='left')
join2.drop(['Application_Calendar_Year', 'Calendar_Instance_Year'], axis=1, inplace = True)

join2.rename(index=str, columns={'Application_Status_Description' : 'Fin_Appl_Status_Description'}, inplace=True)


# application_data['Firm_Offers'] = application_data['Firm_Offers'].map(lambda x: change_greater_than_zero_to_one(x))
# application_data = application_data[application_data['Gender'] != 'UNKNOWN']
