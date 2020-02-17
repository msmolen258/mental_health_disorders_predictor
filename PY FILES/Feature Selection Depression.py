#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


# # 1. Load a prapared data
data =pd.read_excel("prepareddata.xlsx") 
print (data.head())
data = data.drop(columns=['Unnamed: 0'])


# # 2. Create colum data['depression'] (target variable)
# SET TARGET VARIABLE 
# Depression ( yes = 1 , no = 0 )
data.loc[~data['diagnosis'].str.contains('Depression', case=True), 'diagnosis'] = "No"
data.loc[data['diagnosis'].str.contains('Depression', case=True), 'diagnosis'] = "Yes"

# encoding
data['depression'] = data['diagnosis'].map( {'Yes':1, 'No':0} )
data = data.drop(columns=['diagnosis'])


# target variable and features
target = data['depression']
features = data.drop(columns=['depression'])


# # 3. Apply SelectKBest class 
#apply SelectKBest class to extract top 10 best features
bestfeatures = SelectKBest(score_func=chi2, k=20)
X = features
y = target 

fit = bestfeatures.fit(X,y)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)

#concat two dataframes for better visualization 
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']  #naming the dataframe columns
print(featureScores.nlargest(20,'Score'))  #print 20 best features


# # 4.Create Dataframe based on SelectKBest
df1 = data[['depression', 
            'maritalStatus_Married',
            'MentalIllnesspast_depression', 
            'ageAtAdmissiongroup',
            'occupation_Student',
            'employmentStatus_Self-employed', 
            'Male',
            'employmentStatus_Employed',
            'psychoactiveSubType_Marijuana', 
            'fatherDeceased',
            'suicideType_Egoistic suicide', 
            'chronicIllness_High Blood Pressure',
            'useOfMobile',
            'highestEdu',
            'motherDeceased',
            'occupation_Service and sales workers',
            'presentLiving_Civil partner ',
            'occupation_Managers and Professionals',
            'forensicIssue_Arrests', 
            'suicideType_Fatalistic suicide', 
            'chronicIllness_Diabetes' ]]


df1.to_excel("depression.xlsx")  

