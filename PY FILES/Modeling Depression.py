# Load libraries
import pandas as pd
import numpy as np
np.set_printoptions(threshold=np.inf)

from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVR
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


# ## 1.Load dataframe 
data =pd.read_excel("depression.xlsx")
data = data.drop(columns=['Unnamed: 0'])

#Print names of all selected features
for col in data.columns: 
    print(col) 

print()

# ## 2. Split data into test and train and test the models

from sklearn.model_selection import train_test_split

#Split data into train and test
X = data.drop(columns=['depression'],axis=1)
y = data["depression"]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.2, random_state=1, shuffle=True)


# # prepare models
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))



# evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=1)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

    
# Compare Algorithms

pyplot.boxplot(results, labels=names)
pyplot.title('Algorithm Comparison')
pyplot.show()


# ## 3.Tunning The Model’s Hyperparameters

import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

#features and label
features = data.drop(columns=['depression'])
labels = data['depression']


def print_results(results):
    print('BEST PARAMS: {}\n'.format(results.best_params_))

    means = results.cv_results_['mean_test_score']
    stds = results.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, results.cv_results_['params']):
        print('{} (+/-{}) for {}'.format(round(mean, 3), round(std * 2, 3), params))

svc = SVC()
parameters = {
    'kernel': ['linear', 'rbf'],
    'C': [0.1, 1, 10,100]
}

cv = GridSearchCV(svc, parameters, cv=5)
cv.fit(features, labels.values.ravel())

print_results(cv)

SVM1 = cv.best_estimator_

X_train, X_test, y_train, y_test = train_test_split(data.drop('depression', axis=1),
                                                   data['depression'], test_size=0.20,
                                                   random_state=200)

joblib.dump(cv.best_estimator_, 'SVM_model1.pkl')


#Train the model
SVM1.fit(X_train, y_train)

# Make predictions
y_pred = SVM1.predict(X_test)
print (y_pred)


# ## 4. Evaluation


#Classification report
print(classification_report(y_test, y_pred))


#Confusion matrix
print (confusion_matrix(y_test, y_pred))

print ("True:" , y_test.values[0:25])
print ("Pred:", y_pred[0:25])


# Precision score
print ("Precision score:")
print (precision_score(y_test, y_pred))
print ()

# Accurancy score
print ("Accuracy score:")
print (accuracy_score(y_test, y_pred))
print ()


print (data['depression'].value_counts())




