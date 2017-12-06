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
        
def change_nan_to_negative_one(x):
    if pd.isnull(x):
        x = str(-1)
        
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

def find_urban_rural_from_quintile(x, y, z):
    if z == 'International':
        return 'INT'   
    if x == 'UNKNOWN' and y == 'UNKNOWN':
        return 'UNKNOWN'
    
    if y == 'UNKNOWN':
        if x == '1' or x == '2':
            return 'RURAL'
        elif x == 'IQ':
            return 'INT'
        elif x == '3' or x == '4' or x == '5' or x == '6':
            return 'URBAN'
    else:
        return y
        
                
    


# =============================================================================
# Read in files
# =============================================================================
application_data:pd.DataFrame = pd.read_csv('Admission Application Data.csv')
funding_data:pd.DataFrame = pd.read_csv('Vac Work Information Financial.csv')
residence_data:pd.DataFrame = pd.read_csv('Vac Work Information Residential.csv')
cost_data:pd.DataFrame = pd.read_csv('Vac Work Information CourseFee.csv')
further_application_data:pd.DataFrame = pd.read_csv('Vac Work Information Course Details.csv')


# =============================================================================
# Rename all columns to remove spaces
# =============================================================================
application_data    = application_data.rename(columns=lambda x: x.strip().replace(' ','_'))
funding_data        = funding_data.rename(columns=lambda x: x.strip().replace(' ','_'))
residence_data      = residence_data.rename(columns=lambda x: x.strip().replace(' ','_'))
cost_data           = cost_data.rename(columns=lambda x: x.strip().replace(' ','_'))
further_application_data         = further_application_data.rename(columns=lambda x: x.strip().replace(' ','_'))

# =============================================================================
# Fix datatypes
# =============================================================================
further_application_data['Student_Number'] = further_application_data['Student_Number'].map(lambda x : str(x))

# View counts of items in specific column

# =============================================================================
# Drop and Transfrom from other tables
# =============================================================================

# Funding preparation
funding_data['Application_Status_Description'] = funding_data['Application_Status_Description'].map(lambda x: financial_application_sort_outcome(x))
funding_data.sort_values(by=['Student_Number','Application_Calendar_Year','Application_Status_Description'], ascending = False, inplace=True)
funding_data.drop('Application_Status', axis=1, inplace = True)
funding_data.drop('Funding_Level', axis=1, inplace = True)
funding_data.drop_duplicates(keep='first',subset=['Student_Number', 'Application_Calendar_Year'], inplace = True)

# Residence preparation
residence_data.drop('Res_Application_Status', axis=1, inplace = True)
residence_data['Res_Appl_Status_Description'] = residence_data['Res_Appl_Status_Description'].map(lambda x: residential_application_sort_outcome(x))
residence_data.sort_values(by=['Student_Number', 'Calendar_Instance_Year', 'Res_Appl_Status_Description'], ascending = False, inplace = True)
residence_data.drop_duplicates(keep='first',subset=['Student_Number', 'Calendar_Instance_Year'], inplace = True)

# =============================================================================
# Joins
# =============================================================================
join1:pd.DataFrame = application_data.merge(funding_data, left_on=['Student_Number', 'Calendar_Inst_Year'], right_on=['Student_Number', 'Application_Calendar_Year'], how='left')
join2:pd.DataFrame = join1.merge(residence_data, left_on=['Student_Number', 'Calendar_Inst_Year'], right_on=['Student_Number', 'Calendar_Instance_Year'], how='left')
# =============================================================================
# Drop Date columns from joined tables and rename new columns
# =============================================================================
join2.drop(['Application_Calendar_Year', 'Calendar_Instance_Year'], axis=1, inplace = True)

join2.rename(index=str, columns={'Application_Status_Description' : 'Fin_Appl_Status_Description'}, inplace=True)



merged_data = join2.copy()

further_application_data = further_application_data.merge(cost_data, left_on='Faculty_Name', right_on='Degree', how='left')


further_application_data = further_application_data[pd.isnull(further_application_data['Appl_Completion_Date']) == False]
further_application_data.sort_values(by=['Student_Number', 'Academic_Calendar'], inplace=True)
further_application_data.drop(['Program_Title', 'Program_Code', 'Adm_Appl_Year_Of_Study', 'Program_Cat', 'Attendance_Type', 'Degree'], axis=1, inplace = True)

# =============================================================================
# Fix nan's
# =============================================================================
merged_data['Fin_Appl_Status_Description'] = merged_data['Fin_Appl_Status_Description'].fillna(-1)
merged_data['Res_Appl_Status_Description'] = merged_data['Res_Appl_Status_Description'].fillna(-1)
merged_data['Quintile'] = merged_data['Quintile'].fillna('UNKNOWN')
merged_data['Urban_Rural'] = merged_data['Urban_Rural'].fillna('UNKNOWN')
merged_data['Applicants_that_Registered'] = merged_data['Applicants_that_Registered'].map(lambda x : change_greater_than_zero_to_one(x))

merged_data['Urban_Rural'] = merged_data.apply(lambda x : find_urban_rural_from_quintile(x['Quintile'], x['Urban_Rural'], x['Nationality_Status']), axis = 1)

x1 = further_application_data[further_application_data['Academic_Calendar'] == 2016]
x = further_application_data['Student_Number'].value_counts()


merged_data['Firm_Offers'] = merged_data['Firm_Offers'].map(lambda x: change_greater_than_zero_to_one(x))
merged_data = merged_data[merged_data['Firm_Offers'] == 1]
merged_data.drop(['Yos', 'New_to_Wits/Returning', 'Firm_Offers'], axis=1, inplace = True)
merged_data['Quintile'] = merged_data['Quintile'].map(lambda x : str(x))

# application_data = application_data[application_data['Gender'] != 'UNKNOWN']

# merged_data.to_excel('Out.xlsx')

join3:pd.DataFrame = merged_data.merge(further_application_data, left_on=['Student_Number', 'Calendar_Inst_Year'], right_on=['Student_Number','Academic_Calendar'], how='left')
