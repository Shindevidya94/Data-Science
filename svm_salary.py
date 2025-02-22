# -*- coding: utf-8 -*-
"""SVM Salary.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-14LnWRXCWA33xP1al5fVcjcA-UJS9ME
"""

from google.colab import drive

drive.mount('/content/drive/')

cd drive/MyDrive/Assignments/

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import *

train=pd.read_csv('SalaryData_Train(1).csv')
train.sample(5)

train.isna().sum().sum()

test=pd.read_csv('SalaryData_Test(1).csv')
test.sample(5)

test.isna().sum().sum()

features_train=train.iloc[:,:-1]
features_test=test.iloc[:,:-1]

y_train=train.iloc[:,-1]
y_test=test.iloc[:,-1]

features_train.dtypes

encode=LabelEncoder()

for i in features_train.columns:
  if features_train[i].dtypes==object:
    features_train[i]=encode.fit_transform(features_train[i])
  else:
    pass

for i in features_test.columns:
  if features_test[i].dtypes==object:
    features_test[i]=encode.fit_transform(features_test[i])
  else:
    pass

features_train

#Normalizing
def norm_values(val):
  z=(val-val.min())/(val.max()-val.min())
  return z

features_train_norm=norm_values(features_train)

features_test_norm=norm_values(features_test)

features_train_norm.head(5)

train.iloc[:,-1].value_counts()

#Linear model
model_linear=SVC(kernel='linear')
model_linear.fit(features_train_norm,y_train)
y_pred_linear=model_linear.predict(features_test_norm)
acc_linear=accuracy_score(y_test,y_pred_linear)
print('accuracy',acc_linear*100)
print('==='*20)
print(classification_report(y_test,y_pred_linear))

#sigmoid model
model_sigmoid=SVC(kernel='sigmoid')
model_sigmoid.fit(features_train_norm,y_train)
y_pred_sigmoid=model_sigmoid.predict(features_test_norm)
acc_sigmoid=accuracy_score(y_test,y_pred_sigmoid)
print('accuracy',acc_sigmoid*100)
print('==='*20)
print(classification_report(y_test,y_pred_sigmoid))

#rbf model
model_rbf=SVC(kernel='rbf')
model_rbf.fit(features_train_norm,y_train)
y_pred_rbf=model_rbf.predict(features_test_norm)
acc_rbf=accuracy_score(y_test,y_pred_rbf)
print('accuracy',acc_rbf*100)
print('==='*20)
print(classification_report(y_test,y_pred_rbf))

#ploy model
model_poly=SVC(kernel='poly')
model_poly.fit(features_train_norm,y_train)
y_pred_poly=model_poly.predict(features_test_norm)
acc_poly=accuracy_score(y_test,y_pred_poly)
print('accuracy',acc_poly*100)
print('==='*20)
print(classification_report(y_test,y_pred_poly))

