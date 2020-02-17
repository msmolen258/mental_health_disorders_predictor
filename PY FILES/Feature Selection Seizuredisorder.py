import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


# Load prepared data
data =pd.read_excel("prepareddata.xlsx")
data.head()
data = data.drop(columns=['Unnamed: 0'])


# SET TARGET VARIABLE 
# Schizophrenia ( yes = 1 , no = 0 )

data.loc[~data['diagnosis'].str.contains('Seizure disorder', case=True), 'diagnosis'] = "No"
data.loc[data['diagnosis'].str.contains('Seizure disorder', case=True), 'diagnosis'] = "Yes"

#encoding
data['seizuredisorder'] = data['diagnosis'].map( {'Yes':1, 'No':0} )
data = data.drop(columns=['diagnosis'])


# target variable and features
target = data['seizuredisorder']
features = data.drop(columns=['seizuredisorder'])

#apply SelectKBest class to extract top 20 best features
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

df1 = data[['seizuredisorder',
            'ageAtAdmissiongroup',
            'occupation_Student',
            'maritalStatus_Married',
            'fatherDeceased',
            'highestEdu',
            'useOfMobile',
            'employmentStatus_Self-employed',
            'motherDeceased',
            'primarySchool_Public',
            'employmentStatus_Employed',
            'psychoactiveSubType_Marijuana',
            'primarySchool_Private',
            'forensicIssue_Arrests',
            'chronicIllness_Seizure',
            'occupation_Managers and Professionals',
            'tribe_Igbo',
            'familyType_Monogamous',
            'presentLiving_Relatives',
            'occupation_Service and sales workers']]
            



df1.to_excel("seizuredisorder.xlsx")  






