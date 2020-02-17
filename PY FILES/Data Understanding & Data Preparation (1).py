#!/usr/bin/env python
# coding: utf-8

# # INITIAL DATA LOADING

# In[1]:


#1.LOAD THE DATA


# In[2]:


# Load libraries
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


# ## 1.DATA UNDERSTANDING

# ### 1.1 Data shape and data types
data =pd.read_excel("MHPatientDetails.xlsx")
#how many rows and columns
print ('Data shape')
print (data.shape)
print()
#first 10 rows dropped - messy values
data= data.drop([0,1,2,3,4,5,6,7,8,9])
# print all column names
print ('Column names:') 
print(data.columns.values)
print()
# print all data types 
print ('Data types:')
print (data.dtypes)
print()
#change data type for int/float for numerical variables
data = data.astype({'yearOfBirth' : 'int64'})
data = data.astype({'ageAtAdmission' : 'int64'})
data = data.astype({'fatherAge' : 'int64'})
data = data.astype({'motherAge' : 'int64'})
data = data.astype({'fatherYearOfDeath' : 'float64'})
data = data.astype({'motherYearOfDeath' : 'float64'})
data = data.astype({'positionAtBirthMother' : 'int64'})
data = data.astype({'positionAtBirthFather' : 'int64'})
data = data.astype({'pastAdmission' : 'int64'})
data = data.astype({'numEpisodes' : 'int64'})


# ### 1.2 Missing Values
# Missing values in a dataset 
mv = data.isnull().sum()/len(data)*100
print()
print("Missing Values:")
print (mv)
print()

# ### 1.3 Outliers
print ('Data describe:')
print (data.describe())  #describe numerical variables 
print()
#ageAtadmission must be checked -> min number -1700 ??
import seaborn as sns
sns.boxplot(x=data['ageAtAdmission'])

## print (data[(data['ageAtAdmission'] < -1000 )]) # check the negative values 
##print (data[(data['ageAtAdmission'] < 0)]) # check the negative values 

# Check outliers for fatherAge
print ('Father age:')
sns.boxplot(x=data['fatherAge']) #fatherAge
plt.show()
# Check outliers for motherAge
print ('MotherAge:')
sns.boxplot(x=data['motherAge']) #motherAge
plt.show()
# Check outliers for positionAtBirthFather
print ('positionAtBirthFather:')
sns.boxplot(x=data['positionAtBirthFather']) #'positionAtBirthFather
plt.show()
# Check outliers for positionAtBirthMother
print ('positionAtBirthMother:')
sns.boxplot(x=data['positionAtBirthMother']) #positionAtBirthMother
plt.show()

# # 2. Dimensionality Reduction - part 1

# ### 2.1 High Correlation Filter - 1st attempt before encoding 

#Correlation between variables before encoding 
# High correlation. if the correlation between a pair of variables is greater than 0.5-0.6, we should seriously consider dropping
plt.figure(figsize=(20,20))
print ("Correlation matrix:") 
sns.heatmap(data.corr())
plt.show()

#print table with correlation values
corr = data.corr()
print ("Correlation values:")
print (corr)

# AgeatAddmision yearofBirth - --0.540341
# fatherAge vs motherAge - 0.515380
# fatherYearOfDeath vs motherYearOfDeath - 0.663769
# positionAtBirthMother vs  positionAtBirthFather  -0.928155

        #DECISION: DROP THESE COLUMNS (ONE FROM EACH PAIR)

data = data.drop(columns=['yearOfBirth', 'motherAge', 'motherYearOfDeath', 'positionAtBirthMother'])


# # 3. Data preparation

# ### 3.1  ageAtAdmission

# typo correction 
data.loc[data['admissionDate'] == '0209-12-18', 'admissionDate'] = '2009-12-18'
data.loc[data['admissionDate'] == '0201-02-13', 'admissionDate'] = '2010-02-13'

# calculation of the correct age
age1= 2009-1971
age2= 2010-1971

# replace incorrect age values
data.loc[data['ageAtAdmission'] == -1762, 'ageAtAdmission'] = age1
data.loc[data['ageAtAdmission'] == -1770, 'ageAtAdmission'] = age2


#Remove rows with negative age (difficult to replace with mean/median, because it may create false results)  
data = data[(data[['ageAtAdmission']] > 0).all(axis=1)]



sns.boxplot(x=data['ageAtAdmission']) #no negative values
print("ageAtAdmission - after removing negative values:")
plt.show()

# ### 3.2 ocuppation

# Display all rows when ageAtAdmission is lower than 16 and occupation is not equal to 'Student'
    # We assume that if someone is under 16, the occupation the patient should have is a 'Student'.
    # Many inconsistencies found, e.g. row 13 (age: 1, occupation: Business services, maritalStatus: Married).
    # Even if we change occupation to Student, it will be inconsistent with the rest of the variables.
    # DECISION: drop these rows
data = data.drop(data[(data['occupation'].notnull()) & (data['ageAtAdmission'] < 16) & (data['occupation'] != 'Student')].index)

# We assume that someone who is under 3 years old should not have an occupation.
    #Inconsistencies in the data
    #Difficult to decide if the ageAtAdmission, occupation or maritalStatus is wrong
    #DECISION: drop these rows to avoid inconsistencies

data = data.drop(data[(data['ageAtAdmission'] < 3 ) & (data['occupation'].notnull())].index)

# We replace missing values for variable "occupation" with the value "Student" when the following conditions are met:
    #1.ageAtAdmission IS lower than 18
    #2.employmentStatus IS Unemployed
    #3.highestEdu IS NOT "Uneducated"
data.loc[(data['occupation'].isnull()) & (data['ageAtAdmission'] < 18) & (data['employmentStatus'] == 'Unemployed') & (data['highestEdu'] != 'Uneducated')  , 'occupation'] = 'Student'


# Missing values in a dataset for occupation
mocc = data['occupation'].isnull().sum()/len(data)*100
print()
print("Missing Values for occupation column (%):")
print (mocc)

#The rest of the missing values for occupation will be replaced with mode based on highestEdu level that patient has
    #We can check the occupation value that appears the most often for each highestEdu group using groupby() method  
g = data.groupby(['highestEdu'])  
print (g.first()) 

#Based on results replace the missing values for occupation
data.loc[(data['occupation'].isnull()) & (data['highestEdu'] == 'Higher Education') , 'occupation'] = 'Retail and wholesale trade managers'
data.loc[(data['occupation'].isnull()) & (data['highestEdu'] == 'Primary') , 'occupation'] = 'Other clerical support workers'
data.loc[(data['occupation'].isnull()) & (data['highestEdu'] == 'Secondary') , 'occupation'] = 'Professional services managers'
data.loc[(data['occupation'].isnull()) & (data['highestEdu'] == 'Uneducated') , 'occupation'] = 'Professional services managers'


# ### 3.3 maritalStatus

# We assume that a patient under 16 cannot have the maritalStatus = "Married". Rows with these values will be deleted.

data = data.drop(data[(data['ageAtAdmission'] < 16) & (data['maritalStatus'] != 'Never Married')].index)


# ### 3.4 fatherYearofDeath
#Replace the missing values with an appropriate text
         
   # Father Year of Death - not known means "Alive". 
       #To keep the column data type 'numerical:interval', the NaN will be replaced with 0. 
       #For the interval variables when the variable equals 0.0, there is none of that variable.

data["fatherYearOfDeath"]= data["fatherYearOfDeath"].fillna(0)


# ### 3.5 primarySchool, secSechool, tertiarySchool 

# Reason for missing values: level of highest education - patient could not attend specific school 
    # (for ex. higestEdu is "primary school" that means no value for secSchool column etc.)

#If the patient is 'uneducated' that means not attended to any schools 
#so the missing values for primarySchool, secSechool, tertiarySchool if 'highestEdu'='Uneducated' can be replaced with the value 'Not attended'


data.loc[data['highestEdu'] == 'Uneducated', 'primarySchool'] = 'Not attended'
data.loc[data['highestEdu'] == 'Uneducated', 'tertiarySchool'] = 'Not attended'
data.loc[data['highestEdu'] == 'Uneducated', 'secSchool'] = 'Not attended'


#If 'highestEdu'='Primary', then missing values for secSchool and tertiarySchool can be replaced with 'Not attended'
#If 'highestEdu'='Secondary', then missing values for tertiarySchool can be replaced with 'Not attended'


data.loc[data['highestEdu'] == 'Primary', 'secSchool'] = 'Not attended'
data.loc[data['highestEdu'] == 'Primary', 'tertiarySchool'] = 'Not attended'

data.loc[data['highestEdu'] == 'Secondary', 'tertiarySchool'] = 'Not attended'


# any missing values left
mpr = data['primarySchool'].isnull().sum()/len(data)*100
msec= data['secSchool'].isnull().sum()/len(data)*100
mter = data['tertiarySchool'].isnull().sum()/len(data)*100
print("Missing Values:")
print ("primarySchool :" + str(mpr) + " %")
print ("secSchool :" + str(msec) + " %")
print ("tertiarySchool:" + str(mter) + " %")
print()

# Other missing values will be replaced with mode
print ("Mode for primarySchool:")
print (data['primarySchool'].mode())
data.loc[data['primarySchool'].isnull(), 'primarySchool'] = 'Public'

print()
print ("Mode for secSchool:")
print (data['secSchool'].mode()) 
data.loc[data['secSchool'].isnull(), 'secSchool'] = 'Public'

print()
print ("Value counts tertiarySchool:")
print (data['tertiarySchool'].value_counts()) 

data.loc[data['tertiarySchool'].isnull(), 'tertiarySchool'] = 'Public'


# ### 3.6 homicideHis
# If there is no forensic issue, it means there shouldn’t be a homicide history
# The missing values which meet that condition should be replaced with "No"
data.loc[(data['homicideHis'].isnull()) & (data['forensicIssue'] == 'None') , 'homicideHis'] = 'No'

#Replace the rest missing values with mode
print ()
print ("Mode for homicideHis:")
print (data['homicideHis'].mode())
data.loc[(data['homicideHis'].isnull()) & (data['forensicIssue'] != 'None') , 'homicideHis'] = 'No'


# ### 3.7 psychoactiveSubAge & psychoactiveSubType
# Missing values for psychoactiveSubAge and psychoactiveSubType - not known because psychoactiveSub not used
        #(see column psychoactiveSubUse)
        # To replace with 'False'

data["psychoactiveSubAge"]= data["psychoactiveSubAge"].fillna('False')
data["psychoactiveSubType"]= data["psychoactiveSubType"].fillna('False')


# ### 3.8 typeMentalIllness
#Missing values for typeMentalIllness because mentalIllnessHis is false 
        # To replace with "False" 
data["typeMentalIllness"]= data["typeMentalIllness"].fillna('False')


# ### 3.9 familyMentalType
#Missing familyMentalType because familyMentalIllnessHis is false
    # To replace with "False"
data["familyMentalType"]= data["familyMentalType"].fillna('False')


# ### 3.10 suicideType 
#4.2.5 Missing suicideType because suicideHis is false
   # To replace with "False" 
data["suicideType"]= data["suicideType"].fillna('False')


# ### 3.11 fatherAge 

q1 = data['fatherAge'].quantile(0.25)
q3 = data['fatherAge'].quantile(0.75)
iqr = q3-q1 #Interquartile range
fence_low  = q1-1.5*iqr
fence_high = q3+1.5*iqr

print()
print ("fatherAge Q1: " + str(q1))
print ("fatherAge Q3: " + str(q3))
print ("Fence high: " + str(fence_high))
print ("Fence low: " + str(fence_low))

# calculate median for fatherAge
medianfather = data['fatherAge'].median()

# We assume that someone can become a father at least 16 years old. 
#To eliminate false data from our dataset, all values below 16 will be replaced by the median value.
data.loc[data['fatherAge'] < 16, 'fatherAge'] = 20

# lets check the outliers again now
q1 = data['fatherAge'].quantile(0.05)
q3 = data['fatherAge'].quantile(0.95)
iqr = q3-q1 #Interquartile range
fence_high = q3+1.5*iqr
print()
print ("Q1: " + str(q1))
print ("Q3: " + str(q3))
print ("High fence: " + str(fence_high))

# The high fence is very high 157.5 - not posible to represent the age
# DECISION: 3rd quartile treated as maximum value - all values above replaced woth median
data.loc[data['fatherAge'] > 75, 'fatherAge'] = medianfather


# ### 3.12 patientHouseType
#only 6% of missing data
# replace with mode
print ('Value counts patientHouseType')
print (data['patientHouseType'].value_counts())
data.loc[(data['patientHouseType'].isnull()), 'patientHouseType'] = 'Flat Duplex'

#4.CHECK MISSING VALUES AGAIN
# Missing values in a dataset 
mv2 = data.isnull().sum()/len(data)*100
print()
print("Missing Values:")
print (mv2)

#Drop columns with significant missing data 
data = data.drop(columns=['hospitalId', 'carePathway', 'truancyHis', 'fatherReason', 'motherReason'])
data = data.drop(columns=['numEpisodes']) #useless when standing alone


# ### 3.13 presentLiving
print ('Value counts presentLiving')
print (data['presentLiving'].value_counts())
print() 
# Unkown treated as 0, it doesn't give us any information
# Replaced with mode
data.loc[data['presentLiving'].str.contains('Unknown', case=False), 'presentLiving'] = 'Family'


# ### 3.14 religion
print ('Value counts religion')
print (data['religion'].value_counts())
print () 
# Unkown treated as 0, it doesn't give us any information
# Replaced with mode
data.loc[data['religion'].str.contains('Unknown', case=False), 'religion'] = 'Christian'

# ### 3.15 useOfMobile
print ('Value counts useOfmobile')
data['useOfMobile'].value_counts() 
print()
# Unkown treated as 0, it doesn't give us any information
# Replaced with mode
data.loc[data['useOfMobile'].str.contains('Unknown', case=False), 'useOfMobile'] = 'Medium'


# ## High cardinality

# ### 3.16 occupation
# occupation column values splitted between 10 occupation groups (International Standard Classification of Occupations)
data.loc[data['occupation'].str.contains('prof', case=False) | data['occupation'].str.contains('mana', case=False) | data['occupation'].str.contains('senior', case=False), 'occupation'] = 'Managers and Professionals'
data.loc[data['occupation'].str.contains('armed', case=False), 'occupation'] = 'Armed forces'
data.loc[data['occupation'].str.contains('service', case= False) |  data['occupation'].str.contains('sales', case= False) |  data['occupation'].str.contains('care', case= False), 'occupation']= 'Service and sales workers'
data.loc[data['occupation'].str.contains('Clean', case= False) |  data['occupation'].str.contains('Labourers', case= False) |  data['occupation'].str.contains('food', case= False)|  data['occupation'].str.contains('elem', case= False),'occupation'] = 'Elementary occupations'
data.loc[data['occupation'].str.contains('assem', case=False) | data['occupation'].str.contains('plant', case=False), 'occupation'] = 'Plant and machine operators and assemblers'
data.loc[data['occupation'].str.contains('craft', case=False) | data['occupation'].str.contains('building', case=False) | data['occupation'].str.contains('machinery', case=False) | data['occupation'].str.contains('electric', case=False)  , 'occupation'] = 'Craft and related trades workers'
data.loc[data['occupation'].str.contains('clerk', case=False) | data['occupation'].str.contains('clerical', case=False) , 'occupation'] = 'Clerical support workers'
data.loc[data['occupation'].str.contains('forest', case=False) | data['occupation'].str.contains('agricultural', case=False) |  data['occupation'].str.contains('fish', case=False), 'occupation'] = 'Skilled agricultural, forestry and fishery workers'

print ("New occupation:")
print (data['occupation'].unique())
print ()


# ### 3.17 diagnosis

data.loc[data['diagnosis'].str.contains('Sch', case=False), 'diagnosis'] = 'Schizophrenia'
data.loc[data['diagnosis'].str.contains('demen', case=False), 'diagnosis'] = 'Dementia'
data.loc[data['diagnosis'].str.contains('depre', case=False), 'diagnosis'] = 'Depression'
data.loc[data['diagnosis'].str.contains('auti', case=False), 'diagnosis'] = 'Autism'
data.loc[data['diagnosis'].str.contains('Seizure', case=False), 'diagnosis'] = 'Seizure disorder'
data.loc[data['diagnosis'].str.contains('Psychotic', case=False), 'diagnosis'] = 'psychotic disorder'
data.loc[data['diagnosis'].str.contains('anx', case=False), 'diagnosis'] = 'Anxiety disorder'
data.loc[data['diagnosis'].str.contains('mbd', case=False), 'diagnosis'] = 'MBD'
data.loc[data['diagnosis'].str.contains('bipo', case=False), 'diagnosis'] = 'Bipolar'
data.loc[data['diagnosis'].str.contains('hall', case=False), 'diagnosis'] = 'Hallucination'
data.loc[data['diagnosis'].str.contains('adh', case=False), 'diagnosis'] = 'ADHD'
data.loc[data['diagnosis'].str.contains('organic', case=False), 'diagnosis'] = 'Organic mental disorder'
data.loc[(~data["diagnosis"].str.contains('Depression')) & (~data["diagnosis"].str.contains('Schizophrenia')) & (~data["diagnosis"].str.contains('Dementia')) & (~data["diagnosis"].str.contains('Autism')) & (~data["diagnosis"].str.contains('No')) & (~data["diagnosis"].str.contains('Seizure disorder')) & (~data["diagnosis"].str.contains('psychotic disorder')) & (~data["diagnosis"].str.contains('Anxiety disorder')) & (~data["diagnosis"].str.contains('MBD')) & (~data["diagnosis"].str.contains('Bipolar')) & (~data["diagnosis"].str.contains('Hallucination')) & (~data["diagnosis"].str.contains('ADHD'))  &  (~data["diagnosis"].str.contains('Organic mental disorder')) , 'diagnosis'] = 'Other'
data.loc[data['diagnosis'].str.contains('No obvious psychopathy', case=False), 'diagnosis'] = 'Other'

print ("New diagnosis:")
print (data['diagnosis'].unique())
print ()

# ### 3.18 chronicIllness

data.loc[data['chronicIllness'].str.contains('hyperten', case=False), 'chronicIllness'] = 'High Blood Pressure'
data.loc[data['chronicIllness'].str.contains('hiv', case=False) | data['chronicIllness'].str.contains('aids', case=False), 'chronicIllness'] = 'HIV'
data.loc[data['chronicIllness'].str.contains('diab', case=False), 'chronicIllness'] = 'Diabetes'
data.loc[data['chronicIllness'].str.contains('tuberculosis', case=False), 'chronicIllness'] = 'Tuberculosis'
data.loc[data['chronicIllness'].str.contains('typhoid', case=False), 'chronicIllness'] = 'Typhoid'
data.loc[data['chronicIllness'].str.contains('head', case=False), 'chronicIllness'] = 'Head injury'
data.loc[data['chronicIllness'].str.contains('seizure', case=False), 'chronicIllness'] = 'Seizure'
data.loc[data['chronicIllness'].str.contains('Asthma', case=False), 'chronicIllness'] = 'Asthma'
data.loc[data['chronicIllness'].str.contains('sleep', case=False) | data['chronicIllness'].str.contains('insom', case=False), 'chronicIllness'] = 'Problem with sleep'
data.loc[data['chronicIllness'].str.contains('Convul', case=False), 'chronicIllness'] = 'Convulsion'
data.loc[(data['chronicIllness'] == '[]') , 'chronicIllness'] = 'None'
data.loc[(~data["chronicIllness"].str.contains('High Blood Pressure')) & (~data["chronicIllness"].str.contains('HIV')) & (~data["chronicIllness"].str.contains('Diabetes')) & (~data["chronicIllness"].str.contains('Tuberculosis')) & (~data["chronicIllness"].str.contains('None')) & (~data["chronicIllness"].str.contains('Typhoid')) & (~data["chronicIllness"].str.contains('Head injury')) & (~data["chronicIllness"].str.contains('Seizure')) & (~data["chronicIllness"].str.contains('Asthma')) & (~data["chronicIllness"].str.contains('Problem with sleep')) & (~data["chronicIllness"].str.contains('Convulsion')), 'chronicIllness'] = 'Other'


print ("New chronicIllness")
print (data['chronicIllness'].unique())
print ()

# ### 3.19  ageAtAdmission'

#Creating the different age groups
#First group 0 - 20

data['ageAtAdmissiongroup'] = data['ageAtAdmission']

data['ageAtAdmissiongroup'] = np.where((data['ageAtAdmission'] <= 20), #Identifies the case to apply to
                           '0 - 20',      #This is the value that is inserted
                           data['ageAtAdmissiongroup'])      #This is the column that is affected


#Second group 21-30
data['ageAtAdmissiongroup'] = np.where((data['ageAtAdmission'] >= 21)
                           & (data['ageAtAdmission'] <= 30), #Identifies the case to apply to
                           '21 - 30',      #This is the value that is inserted
                           data['ageAtAdmissiongroup'])      #This is the column that is affected
#Third group 31-40

data['ageAtAdmissiongroup'] = np.where((data['ageAtAdmission'] >= 31)
                           & (data['ageAtAdmission'] <= 40), #Identifies the case to apply to
                           '31 - 40',      #This is the value that is inserted
                           data['ageAtAdmissiongroup'])      #This is the column that is affected
#Fourth group 41-60

data['ageAtAdmissiongroup'] = np.where((data['ageAtAdmission'] >= 41)
                           & (data['ageAtAdmission'] <= 60), #Identifies the case to apply to
                           '41 - 60',      #This is the value that is inserted
                           data['ageAtAdmissiongroup'])      #This is the column that is affected

#Fifth group +60

data.loc[data['ageAtAdmission'] > 60, 'ageAtAdmissiongroup'] = '60+'


#Now we can drop old column 'ageAtAdmission'
data = data.drop(['ageAtAdmission'], axis=1)


# ### 3.20 fatherAge

data['fatherAgegroups'] = data['fatherAge']

#First group 
data['fatherAgegroups'] = np.where((data['fatherAge'] >= 16)
                           & (data['fatherAge'] <= 40), #Identifies the case to apply to
                           '16 - 40',      #This is the value that is inserted
                           data['fatherAgegroups'])      #This is the column that is affected
# Second group

data['fatherAgegroups'] = np.where((data['fatherAge'] >= 41)
                           & (data['fatherAge'] <= 60), #Identifies the case to apply to
                           '41 - 60',      #This is the value that is inserted
                           data['fatherAgegroups'])      #This is the column that is affected
#Third group

data.loc[data['fatherAge'] > 60, 'fatherAgegroups'] = '60+'

#Now we can drop old column 'fatherAge'
data = data.drop(['fatherAge'], axis=1)


# ### 3.21 pastAdmission
data['pastAdmissiongr'] = data['pastAdmission']

# None
data['pastAdmissiongr'] = np.where((data['pastAdmission'] == 0), #Identifies the case to apply to
                           'None',      #This is the value that is inserted
                           data['pastAdmissiongr'])      #This is the column that is affected

# lower than 5
data['pastAdmissiongr'] = np.where((data['pastAdmission'] > 0) & (data['pastAdmission'] < 5), #Identifies the case to apply to
                           '1-5',      #This is the value that is inserted
                           data['pastAdmissiongr'])      #This is the column that is affected   
# 5 and more
data['pastAdmissiongr'] = np.where((data['pastAdmission'] >= 5), #Identifies the case to apply to
                           '5+',      #This is the value that is inserted
                           data['pastAdmissiongr'])      #This is the column that is affected   


# ### 3.22 positionatBirth

Q1 = data['positionAtBirthFather'].quantile(0.05)
Q3 = data['positionAtBirthFather'].quantile(0.95)
IQR = Q3 - Q1
fence_low  = Q1-1.5*IQR
fence_high = Q3+1.5*IQR


print ("Q1 positionAtBirthFather: " + str(Q1))
print ("Q3 positionAtBirthFather: " + str(Q3))
print ("Fence high: ", fence_high)
print ("Fencelow: ", fence_low)
print ()


medianpos = data['positionAtBirthFather'].median()
data.loc[data['positionAtBirthFather'] > 15, 'positionAtBirthFather'] = medianpos

data['positionAtBirth'] = data['positionAtBirthFather']

#First child
data['positionAtBirth'] = np.where((data['positionAtBirthFather'] == 0), #Identifies the case to apply to
                           'First child',      #This is the value that is inserted
                           data['positionAtBirth'])      #This is the column that is affected
# Not first child

data['positionAtBirth'] = np.where((data['positionAtBirthFather'] != 0), #Identifies the case to apply to
                           'Not first child',      #This is the value that is inserted
                           data['positionAtBirth'])      #This is the column that is affected   


data.drop(['positionAtBirthFather'], axis=1, inplace = True)


# # 4. Dimensionality Reduction - part 2

# ### 4.1 Columns definitely not related to our model - DROP
#Drop columns which are NOT necessary for our model ( Hostpital Admin group)

data = data.drop(columns=['timeStamp', 'id', 'admissionDate' ,'pastAdmission', 'accompaniedPerson', 'personStayWithPatient', 'patientHouseType', 'referral'])

# NOT A LIFESTYLE FACTOR
data.drop(['medication'], axis=1, inplace = True)
data.drop(['complaints'], axis=1, inplace = True)


# ### 4.2 Grouping variables that give the same information.

# suicideHis and suicideType
# After replacing the missing values in this column, they both give us the same information.
# DECISION:  Column suicideHis can be dropped
data = data.drop(columns=['suicideHis']) 

#mentalIllnessHis and typeMentalIllness
# After replacing the missing values in this column, they both give us the same information.
# DECISION:  Column mentalIllnessHis can be dropped
data = data.drop(columns=['mentalIllnessHis']) 


# psychoactiveSubUse', 'psychoactiveSubAge' and 'psychoactiveSubType
# After replacing the missing values in this column, column psychoactiveSubUse' and 'psychoactiveSubType give us the same information
# DECISION:  Column psychoactiveSubUse can be dropped
data = data.drop(columns=['psychoactiveSubUse', 'psychoactiveSubAge']) 


#familyMentalIllnessHis', 'familyMentalType
# After replacing the missing values in this column, they both give us the same information.
# DECISION:  Column familyMentalIllnessHis can be dropped
data = data.drop(columns=['familyMentalIllnessHis']) 

print()
print("Data shape after all corrections:")
print (data.shape)
print ()

# # 5. ENCODING 

#ORDINAL ENCODING 

#Encode ageAtAdmissiongroup

# Create mapper
age_mapper = {  '0 - 20':1, 
                '21 - 30':2,
                '31 - 40':3,
                '41 - 60':4,
                '60+':5}

data['ageAtAdmissiongroup'] = data['ageAtAdmissiongroup'].replace(age_mapper)

#Encode fatherAgegroup

# Create mapper
age_mapper = {  
                '16 - 40':1,
                '41 - 60':2,
                '60+':3}

data['fatherAgegroups'] = data['fatherAgegroups'].replace(age_mapper)

#Encode highestEdu

# Create mapper
he_mapper = {  'Uneducated':1, 
                'Primary':2,
                'Secondary':3,
                'Higher Education':4}

data['highestEdu'] = data['highestEdu'].replace(he_mapper)


#Encode useOfMobile

# Create mapper
usem_mapper = {  'none':1, 
                'low':2,
                'Medium':3,
                'High':4,
               'Very High':5,
              }

data['useOfMobile'] = data['useOfMobile'].replace(usem_mapper)


#Encode useOfSocialMedia	 (Ordinal encoding)

# Create mapper
usesm_mapper = {  'none':1, 
                'low':2,
                'Medium':3,
                'High':4,
               'Very High':5,
               'Unknown' : 6
              }

data['useOfSocialMedia'] = data['useOfSocialMedia'].replace(usesm_mapper)

#Encode pastAdmissiongr	 (Ordinal encoding)

# Create mapper
padm_mapper = {  'None':1, 
                '1-5':2,
                '5+':3}

data['pastAdmissiongr'] = data['pastAdmissiongr'].replace(padm_mapper)


#BINARY Values
data['Male'] = data['gender'].map( {'Male':1, 'Female':0, 'Others':3} )
data = data.drop(columns=['gender']) 
data['fatherDeceased'] = data['fatherDeceased'].map( {'true':1, 'false':0} )
data['motherDeceased'] = data['motherDeceased'].map( {'true':1, 'false':0} )
data['fatherUnknownYearOfDeath'] = data['fatherUnknownYearOfDeath'].map( {'true':1, 'false':0} )
data['motherUnknownYearOfDeath'] = data['motherUnknownYearOfDeath'].map( {'true':1, 'false':0} )
data['homicideHis'] = data['homicideHis'].map( {'Yes':1, 'No':0} )

# ONE HOT ENCODING

from sklearn.preprocessing import OneHotEncoder

#Encode tribe
data= pd.concat([data, pd.get_dummies(data['tribe'],prefix='tribe')], axis=1)
data.drop(['tribe'], axis=1, inplace = True)

# Encode religion
data= pd.concat([data, pd.get_dummies(data['religion'],prefix='religion')], axis=1)
data.drop(['religion'], axis=1, inplace = True)

# Encode  employmentStatus
data= pd.concat([data, pd.get_dummies(data['employmentStatus'],prefix='employmentStatus')], axis=1)
data.drop(['employmentStatus'], axis=1, inplace = True)

# Encode  familyMentalType
data= pd.concat([data, pd.get_dummies(data['familyMentalType'],prefix='familyMentalType')], axis=1)
data.drop(['familyMentalType'], axis=1, inplace = True)

# Encode suicideType
data= pd.concat([data, pd.get_dummies(data['suicideType'],prefix='suicideType')], axis=1)
data.drop(['suicideType'], axis=1, inplace = True)

# Encode childhoodLiving
data= pd.concat([data, pd.get_dummies(data['childhoodLiving'],prefix='childhoodLiving')], axis=1)
data.drop(['childhoodLiving'], axis=1, inplace = True)

# Encode  presentLiving
data= pd.concat([data, pd.get_dummies(data['presentLiving'],prefix='presentLiving')], axis=1)
data.drop(['presentLiving'], axis=1, inplace = True)

# Encode  maritalStatusMother
data= pd.concat([data, pd.get_dummies(data['maritalStatusMother'],prefix='maritalStatusMother')], axis=1)
data.drop(['maritalStatusMother'], axis=1, inplace = True)

# Encode  maritalStatusFather
data= pd.concat([data, pd.get_dummies(data['maritalStatusFather'],prefix='maritalStatusFather')], axis=1)
data.drop(['maritalStatusFather'], axis=1, inplace = True)

# Encode chronicIllness
data= pd.concat([data, pd.get_dummies(data['chronicIllness'],prefix='chronicIllness')], axis=1)
data.drop(['chronicIllness'], axis=1, inplace = True)

# Encode  typeMentalIllness
data= pd.concat([data, pd.get_dummies(data['typeMentalIllness'],prefix='MentalIllnesspast')], axis=1)
data.drop(['typeMentalIllness'], axis=1, inplace = True)

# Encode psychoactiveSubType
data= pd.concat([data, pd.get_dummies(data['psychoactiveSubType'],prefix='psychoactiveSubType')], axis=1)
data.drop(['psychoactiveSubType'], axis=1, inplace = True)

# Encode familyType
data= pd.concat([data, pd.get_dummies(data['familyType'],prefix='familyType')], axis=1)
data.drop(['familyType'], axis=1, inplace = True)

# Encode forensicIssue
data= pd.concat([data, pd.get_dummies(data['forensicIssue'],prefix='forensicIssue')], axis=1)
data.drop(['forensicIssue'], axis=1, inplace = True)

#Encode primarySchool 
data= pd.concat([data, pd.get_dummies(data['primarySchool'],prefix='primarySchool')], axis=1)
data.drop(['primarySchool'], axis=1, inplace = True)

#Encode secSchool
data= pd.concat([data, pd.get_dummies(data['secSchool'],prefix='secSchool')], axis=1)
data.drop(['secSchool'], axis=1, inplace = True)

#Encode tertiarySchool
data= pd.concat([data, pd.get_dummies(data['tertiarySchool'],prefix='tertiarySchool')], axis=1)
data.drop(['tertiarySchool'], axis=1, inplace = True)

#Encode occupation
data= pd.concat([data, pd.get_dummies(data['occupation'],prefix='occupation')], axis=1)
data.drop(['occupation'], axis=1, inplace = True)

#Encode maritalStatus
data= pd.concat([data, pd.get_dummies(data['maritalStatus'],prefix='maritalStatus')], axis=1)
data.drop(['maritalStatus'], axis=1, inplace = True)

#Encode positionAtBirth
data= pd.concat([data, pd.get_dummies(data['positionAtBirth'],prefix='positionAtBirth')], axis=1)
data.drop(['positionAtBirth'], axis=1, inplace = True)

# print all data types 
print ('Data types:')
print()

# # 6.Dimensionality Reduction - part 3
df = data.copy()
#drop the target variable
df.drop(['diagnosis'], axis=1, inplace = True)

plt.figure(figsize=(40,40)) 
sns.heatmap(data.corr())
plt.show()
print()

def get_redundant_pairs(df):
    #Get diagonal and lower triangular pairs of correlation matrix
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df, n=5):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

print("Top Absolute Correlations")
print()
print(get_top_abs_correlations(df, 40))



df.drop(['positionAtBirth_Not first child','religion_Islam', 'tertiarySchool_Public', 'forensicIssue_None', 'maritalStatusFather_Never Married',  'maritalStatus_Never Married', 'familyType_polygamous', 'secSchool_Not attended', 'maritalStatusFather_divorced', 'useOfSocialMedia', 'maritalStatusMother_Widow', 'motherUnknownYearOfDeath', 'MentalIllnesspast_psychotic disorders', 'familyMentalType_psychotic disorders', 'secSchool_Public', 'suicideType_False', 'primarySchool_Not attended', 'tertiarySchool_Not attended', 'secSchool_Not attended','childhoodLiving_With both parents','tribe_Yoruba', 'fatherUnknownYearOfDeath', 'fatherYearOfDeath', 'employmentStatus_Unemployed'  ], axis=1, inplace = True)


# # 7. Saving the finished dataframe
# target variable column
tv = data['diagnosis']
# encoded features must be linked with the target variable using concatenation
df1 = pd.concat([df, tv], axis=1)
# Save to excel file
df1.to_excel("prepareddata.xlsx")  

#### END ####

