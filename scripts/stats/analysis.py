#! /usr/bin/env python3
"""
Author: Conor Spicer
Date Created: 4th Jan 2018

To compare: https://github.com/fivethirtyeight/nfl-elo-games
"""
# Import relevant modules
# import nflgame
import numpy as np
import pandas as pd
import sys
sys.path.append('/Users/conorspicer/Documents/Udemy/Django/My_code/predictor/scripts/stats')
from functions import independent_vars

# Read in data and exclude week 1 games
df = pd.read_csv('2009_to_2017_data_complete.csv', index_col=0)
df = df[df.week>1]

# Split data into what we wish to predict from (X) and the 3 variables we aim to predict
X = df[independent_vars].values
win = df['win']
margin = df['margin']
total_pts = df['total_pts']

# Define which variable we want to predict
y = win

# Transform 'home'/ 'away' to OneHot encoded columns
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X , y, test_size = 0.2)
# X_train, X_test, y_train, y_test = train_test_split(X , y, test_size = 0.2, random_state=0)
# X_train, X_test, y_train, y_test = train_test_split(X , y, test_size = 0.2, random_state=0)
# X_train, X_test, y_train, y_test = train_test_split(X , y, test_size = 0.2, random_state=0)

# Feature Scaling, here only applied on independent_vars. Wish to keep 'win' as boolean
# from sklearn.preprocessing import StandardScaler
# sc_X = StandardScaler()
# X_train = sc_X.fit_transform(X_train)
# X_test = sc_X.transform(X_test)

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
(cm[0][0]+cm[1][1])/sum(sum(cm))
# RESULT: 65% prediction accuracy


# Fitting K-NN to the Training set
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
(cm[0][0]+cm[1][1])/sum(sum(cm))
# RESULT: 60% prediction accuracy


# Fitting SVM to the Training set. (Very slow)
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
(cm[0][0]+cm[1][1])/sum(sum(cm))
# RESULT: 65% prediction accuracy


# Fitting Kernel SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf', random_state = 0)
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
(cm[0][0]+cm[1][1])/sum(sum(cm))
# RESULT: 65% prediction accuracy


# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
(cm[0][0]+cm[1][1])/sum(sum(cm))
# RESULT: 64% prediction accuracy

# Fitting Decision Tree Classification to the Training set
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
(cm[0][0]+cm[1][1])/sum(sum(cm))
# RESULT: 55% prediction accuracy

# Fitting Random Forest Classification to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)
# Predicting the Test set results
y_pred = classifier.predict(X_test)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
(cm[0][0]+cm[1][1])/sum(sum(cm))
# RESULT: 60% prediction accuracy
