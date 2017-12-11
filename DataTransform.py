# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# =============================================================================
# Functions used in lambda's
# =============================================================================

def change_greater_than_zero_to_one(x):
    if x > 0:
        return 1
    else:
        return 0


def change_application_count(x):
    if x > 3:
        return 2
    elif x > 0:
        return 1
    else:
        return 0


def change_UNKNOWN_to_negative_one(x):
    if x == 'UNKNOWN':
        return -1
    else:
        return x


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


def find_if_taken_gap_year(x):
    if x == 'Current Matric':
        return '0'
    elif x == 'Unknown':
        return 'UNKNOWN'
    else:
        return '1'


def change_to_unique_value(x, g):
    return g.index(x)


def change_race(x):
    if x == 'AFRICAN':
        return x
    elif x == 'WHITE':
        return x
    else:
        return 'OTHER'


def check_if_applied(x):
    # print(cols, '\t', x[3], '\t', x[2])
    if x[-1] is False:
        return -1
    else:
        if x[2] == 'Accepted':
            return 1
        else:
            return 0




# =============================================================================
# Read in files
# =============================================================================
application_data:pd.DataFrame = pd.read_csv('Admission Application Data.csv')
funding_data:pd.DataFrame = pd.read_csv('Vac Work Information Financial.csv')
residence_data:pd.DataFrame = pd.read_csv('Vac Work Information Residential.csv')
#cost_data:pd.DataFrame = pd.read_csv('Vac Work Information CourseFee.csv')
further_application_data:pd.DataFrame = pd.read_csv('Vac Work Information Course Details.csv')
faculty_data:pd.DataFrame = pd.read_csv('Vac Work Information Course Details new.csv')


# =============================================================================
# Rename all columns to remove spaces
# =============================================================================
application_data    = application_data.rename(columns=lambda x: x.strip().replace(' ','_'))
funding_data        = funding_data.rename(columns=lambda x: x.strip().replace(' ','_'))
residence_data      = residence_data.rename(columns=lambda x: x.strip().replace(' ','_'))
#cost_data          = cost_data.rename(columns=lambda x: x.strip().replace(' ','_'))
faculty_data        = faculty_data.rename(columns=lambda x: x.strip().replace(' ','_'))
further_application_data         = further_application_data.rename(columns=lambda x: x.strip().replace(' ','_'))

# =============================================================================
# Fix datatypes
# =============================================================================
further_application_data['Student_Number'] = further_application_data['Student_Number'].map(lambda x : str(x))
faculty_data['Student_Number'] = faculty_data['Student_Number'].map(lambda x : str(x))

faculty_data = faculty_data.fillna('Declined')
faculty_data = faculty_data.sort_values(by=['Student_Number', 'Academic_Calendar', 'Faculty_Name'])


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

further_application_data.drop(['Faculty_Name', 'Program_Title', 'Program_Code', 'Adm_Appl_Year_Of_Study', 'Program_Cat', 'Adm_Appl_Number', 'Adm_Offer_Resp_Date', 'Adm_Offer_Resp_Status', 'Appl_Completion_Date', 'Outcome_Decision_Date', 'Appl_Creation_Date'], axis=1, inplace = True)
further_application_data.sort_values(by=['Student_Number','Academic_Calendar'], inplace=True)
further_application_data.drop_duplicates(keep='first', subset=['Student_Number', 'Academic_Calendar'], inplace = True)
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
join3:pd.DataFrame = join2.merge(further_application_data, left_on=['Student_Number', 'Calendar_Inst_Year'], right_on=['Student_Number','Academic_Calendar'], how='left')


merged_data:pd.DataFrame = join3.copy()

# =============================================================================
# Fix nan's
# =============================================================================


merged_data['Fin_Appl_Status_Description'] = merged_data['Fin_Appl_Status_Description'].fillna('UNKNOWN')
merged_data['Res_Appl_Status_Description'] = merged_data['Res_Appl_Status_Description'].fillna('UNKNOWN')
merged_data['Age'] = merged_data['Age'].fillna('UNKNOWN')
merged_data = merged_data.fillna('UNKNOWN')

merged_data = merged_data[merged_data['Applicants_that_Registered'] != 'UNKNOWN']

merged_data['Applicants_that_Registered'] = merged_data['Applicants_that_Registered'].map(lambda x : change_application_count(x))


merged_data['Firm_Offers'] = merged_data['Firm_Offers'].map(lambda x: change_greater_than_zero_to_one(x))
merged_data['Adm_Appl_Special_Group_1'] = merged_data['Adm_Appl_Special_Group_1'].map(lambda x: find_if_taken_gap_year(x))
merged_data['Application_Received'] = merged_data['Application_Received'].map(lambda x: change_application_count(x))
merged_data['Race'] = merged_data['Race'].map(lambda x: change_race(x))
merged_data = merged_data[merged_data['Firm_Offers'] == 1]
merged_data.drop(['Yos', 'New_to_Wits/Returning', 'Firm_Offers', 'UG_/_PG_Code_Desc', 'Applicants_(Drilling_into_dimensions_will_change_stats)','Firm_Offers_Accepted' , 'Academic_Calendar', 'Descr', ], axis=1, inplace = True)
merged_data['Quintile'] = merged_data['Quintile'].map(lambda x : str(x))
merged_data['Age'] = merged_data['Age'].map(lambda x : int(x))
merged_data = merged_data[merged_data['Age'] < 75]
merged_data = merged_data[merged_data['Age'] > 14]
merged_data['Adm_Appl_Special_Group_1'] = merged_data['Adm_Appl_Special_Group_1'].map(lambda x : change_UNKNOWN_to_negative_one(x))

merged_data = merged_data[merged_data['Nationality_Status'] == 'South African']

merged_data = merged_data[merged_data['Quintile'] != 'UNKNOWN']
merged_data = merged_data[merged_data['Race'] != 'UNKNOWN']
merged_data = merged_data[merged_data['Gender'] != 'UNKNOWN']
merged_data = merged_data[merged_data['Matric_Province'] != 'UNKNOWN']
merged_data = merged_data[merged_data['Urban_Rural'] != 'UNKNOWN']
merged_data = merged_data[merged_data['Fin_Appl_Status_Description'] != 'UNKNOWN']
merged_data = merged_data[merged_data['Res_Appl_Status_Description'] != 'UNKNOWN']

merged_data = merged_data[merged_data['Admission_Ratings'] >= 20]
# merged_data = merged_data[merged_data['School_name'] != 'UN']

merged_data.drop(['School_name', 'Nationality_Status'],axis=1, inplace=True)


# =============================================================================
# Faculty information
# =============================================================================
merged_data.rename(index=str, columns={'Calendar_Inst_Year' : 'Academic_Calendar', 'Adm_Appl_Special_Group_1' : 'Gap_Year'}, inplace=True)
combination_data = merged_data.merge(faculty_data, left_on=['Student_Number', 'Academic_Calendar'], right_on=['Student_Number', 'Academic_Calendar'], how = 'left')

combination_data['Faculty_of_Humanities'] = (combination_data['Faculty_Name'] == 'Faculty of Humanities - Total')
combination_data['Faculty_of_Science'] = (combination_data['Faculty_Name'] == 'Faculty of Science - Total')
combination_data['Faculty_of_Health_Sciences'] = (combination_data['Faculty_Name'] == 'Faculty of Health Sciences - Total')
combination_data['Faculty_of_Engineering_and_the_Built_Environment'] = (combination_data['Faculty_Name'] == 'Faculty of Engineering and the Built Environment - Total')
combination_data['Faculty_of_Commerce,_Law_&_Management'] = (combination_data['Faculty_Name'] == 'Faculty of Commerce, Law & Management - Total')


# =============================================================================
# Faculty Apllied and Accepted
# =============================================================================
cd_humainities = combination_data.copy()
cd_humainities.sort_values(by=['Student_Number', 'Academic_Calendar', 'Faculty_of_Humanities'], ascending = False ,inplace=True)
cd_humainities.drop_duplicates(keep='first',subset=['Student_Number', 'Academic_Calendar'], inplace = True)
merged_data = merged_data.merge(cd_humainities[['Student_Number', 'Academic_Calendar','Faculty_of_Humanities']], left_on=['Student_Number', 'Academic_Calendar'], right_on=['Student_Number', 'Academic_Calendar'], how='left')

cd_responce = combination_data[['Student_Number','Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Humanities']].copy()
cd_responce.sort_values(by=['Student_Number', 'Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Humanities'], ascending = False ,inplace=True)
cd_responce['Faculty_of_Humanities_Responce'] = cd_responce.apply(lambda x : check_if_applied(x), axis=1)
cd_responce = cd_responce.drop_duplicates(keep='first', subset=['Student_Number', 'Academic_Calendar'])
merged_data = merged_data.merge(cd_responce[['Student_Number', 'Academic_Calendar', 'Faculty_of_Humanities_Responce']], on=['Student_Number', 'Academic_Calendar'], how='left')

cd_humainities = combination_data.copy()
cd_humainities.sort_values(by=['Student_Number', 'Academic_Calendar', 'Faculty_of_Science'], ascending = False ,inplace=True)
cd_humainities.drop_duplicates(keep='first',subset=['Student_Number', 'Academic_Calendar'], inplace = True)
merged_data = merged_data.merge(cd_humainities[['Student_Number', 'Academic_Calendar','Faculty_of_Science']], left_on=['Student_Number', 'Academic_Calendar'], right_on=['Student_Number', 'Academic_Calendar'], how='left')

cd_responce = combination_data[['Student_Number','Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Science']].copy()
cd_responce.sort_values(by=['Student_Number', 'Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Science'], ascending = False ,inplace=True)
cd_responce['Faculty_of_Science_Responce'] = cd_responce.apply(lambda x : check_if_applied(x), axis=1)
cd_responce = cd_responce.drop_duplicates(keep='first', subset=['Student_Number', 'Academic_Calendar'])
merged_data = merged_data.merge(cd_responce[['Student_Number', 'Academic_Calendar', 'Faculty_of_Science_Responce']], on=['Student_Number', 'Academic_Calendar'], how='left')

cd_humainities = combination_data.copy()
cd_humainities.sort_values(by=['Student_Number', 'Academic_Calendar', 'Faculty_of_Health_Sciences'], ascending = False ,inplace=True)
cd_humainities.drop_duplicates(keep='first',subset=['Student_Number', 'Academic_Calendar'], inplace = True)
merged_data = merged_data.merge(cd_humainities[['Student_Number', 'Academic_Calendar','Faculty_of_Health_Sciences']], left_on=['Student_Number', 'Academic_Calendar'], right_on=['Student_Number', 'Academic_Calendar'], how='left')

cd_responce = combination_data[['Student_Number','Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Health_Sciences']].copy()
cd_responce.sort_values(by=['Student_Number', 'Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Health_Sciences'], ascending = False ,inplace=True)
cd_responce['Faculty_of_Health_Sciences_Responce'] = cd_responce.apply(lambda x : check_if_applied(x), axis=1)
cd_responce = cd_responce.drop_duplicates(keep='first', subset=['Student_Number', 'Academic_Calendar'])
merged_data = merged_data.merge(cd_responce[['Student_Number', 'Academic_Calendar', 'Faculty_of_Health_Sciences_Responce']], on=['Student_Number', 'Academic_Calendar'], how='left')

cd_humainities = combination_data.copy()
cd_humainities.sort_values(by=['Student_Number', 'Academic_Calendar', 'Faculty_of_Engineering_and_the_Built_Environment'], ascending = False ,inplace=True)
cd_humainities.drop_duplicates(keep='first',subset=['Student_Number', 'Academic_Calendar'], inplace = True)
merged_data = merged_data.merge(cd_humainities[['Student_Number', 'Academic_Calendar','Faculty_of_Engineering_and_the_Built_Environment']], left_on=['Student_Number', 'Academic_Calendar'], right_on=['Student_Number', 'Academic_Calendar'], how='left')

cd_responce = combination_data[['Student_Number','Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Engineering_and_the_Built_Environment']].copy()
cd_responce.sort_values(by=['Student_Number', 'Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Engineering_and_the_Built_Environment'], ascending = False ,inplace=True)
cd_responce['Faculty_of_Engineering_and_the_Built_Environment_Responce'] = cd_responce.apply(lambda x : check_if_applied(x), axis=1)
cd_responce = cd_responce.drop_duplicates(keep='first', subset=['Student_Number', 'Academic_Calendar'])
merged_data = merged_data.merge(cd_responce[['Student_Number', 'Academic_Calendar', 'Faculty_of_Engineering_and_the_Built_Environment_Responce']], on=['Student_Number', 'Academic_Calendar'], how='left')

cd_humainities = combination_data.copy()
cd_humainities.sort_values(by=['Student_Number', 'Academic_Calendar', 'Faculty_of_Commerce,_Law_&_Management'], ascending = False ,inplace=True)
cd_humainities.drop_duplicates(keep='first',subset=['Student_Number', 'Academic_Calendar'], inplace = True)
merged_data = merged_data.merge(cd_humainities[['Student_Number', 'Academic_Calendar','Faculty_of_Commerce,_Law_&_Management']], left_on=['Student_Number', 'Academic_Calendar'], right_on=['Student_Number', 'Academic_Calendar'], how='left')

cd_responce = combination_data[['Student_Number','Academic_Calendar', 'Adm_Offer_Resp_Status', 'Faculty_of_Commerce,_Law_&_Management']].copy()
cd_responce.sort_values(by=['Student_Number', 'Academic_Calendar', 'Faculty_of_Commerce,_Law_&_Management', 'Adm_Offer_Resp_Status'], ascending = False ,inplace=True)
cd_responce['Faculty_of_Commerce,_Law_&_Management_Responce'] = cd_responce.apply(lambda x : check_if_applied(x), axis=1)
cd_responce = cd_responce.drop_duplicates(keep='first', subset=['Student_Number', 'Academic_Calendar'])
merged_data = merged_data.merge(cd_responce[['Student_Number', 'Academic_Calendar', 'Faculty_of_Commerce,_Law_&_Management_Responce']], on=['Student_Number', 'Academic_Calendar'], how='left')


count = merged_data['Faculty_of_Humanities'].value_counts()


# =============================================================================
# Drop student number since it is no longer needed
# =============================================================================
merged_data.drop(['Student_Number'],axis=1, inplace=True)


# Cast true:false as 1:0
merged_data[['Faculty_of_Humanities', 'Faculty_of_Science', 'Faculty_of_Health_Sciences', 'Faculty_of_Engineering_and_the_Built_Environment', 'Faculty_of_Commerce,_Law_&_Management']] = merged_data[['Faculty_of_Humanities', 'Faculty_of_Science', 'Faculty_of_Health_Sciences', 'Faculty_of_Engineering_and_the_Built_Environment', 'Faculty_of_Commerce,_Law_&_Management']].astype(int)


# =============================================================================
# Create a copy of merged_data so that we can keep a version that contains the actual values
# =============================================================================
merged_data_String = merged_data.copy()

# =============================================================================
# Convert string values to numerical values
# =============================================================================
#school_unique = merged_data['School_name'].unique().tolist()
#merged_data['School_name'] = merged_data['School_name'].map(lambda x : change_to_unique_value(x,school_unique))
matric_unique = merged_data['Matric_Province'].unique().tolist()
merged_data['Matric_Province'] = merged_data['Matric_Province'].map(lambda x : change_to_unique_value(x,matric_unique))
race_unique = merged_data['Race'].unique().tolist()
merged_data['Race'] = merged_data['Race'].map(lambda x : change_to_unique_value(x,race_unique))
gender_unique = merged_data['Gender'].unique().tolist()
merged_data['Gender'] = merged_data['Gender'].map(lambda x : change_to_unique_value(x,gender_unique))
# nationality_unique = merged_data['Nationality_Status'].unique().tolist()
# merged_data['Nationality_Status'] = merged_data['Nationality_Status'].map(lambda x : change_to_unique_value(x,nationality_unique))
# quintile_unique = merged_data['Quintile'].unique().tolist()
# merged_data['Quintile'] = merged_data['Quintile'].map(lambda x : change_to_unique_value(x,quintile_unique))
urban_unique = merged_data['Urban_Rural'].unique().tolist()
merged_data['Urban_Rural'] = merged_data['Urban_Rural'].map(lambda x : change_to_unique_value(x,urban_unique))
attendance_unique = merged_data['Attendance_Type'].unique().tolist()
merged_data['Attendance_Type'] = merged_data['Attendance_Type'].map(lambda x : change_to_unique_value(x,attendance_unique))


# =============================================================================
# convert all string-numeric to true-numeric values
# =============================================================================
merged_data = merged_data.apply(pd.to_numeric)


# =============================================================================
# Binarise some of the catagorical columns
# =============================================================================
merged_data_with_dummies = pd.get_dummies(merged_data, columns=['Quintile','Attendance_Type', 'Urban_Rural', 'Fin_Appl_Status_Description','Fin_Appl_Status_Description', 'Matric_Province', 'Gap_Year'])


# =============================================================================
# Export dataframe to xlsx and csv formats
# =============================================================================
merged_data.to_excel('Merged_Data_Numeric.xlsx', index=False)
merged_data_String.to_excel('Merged_Data_String.xlsx', index=False)
merged_data.to_csv('Merged_Data_Numeric.csv', index=False)
merged_data_String.to_csv('Merged_Data_String.csv', index=False)

merged_data_with_dummies.to_csv('Dummies.csv', index=False)