# -*- coding: utf-8 -*-
"""Navie Bayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dl_2_USlImYLfenF98Sbr4TtNKzTnNEc
"""

from google.colab import drive

drive.mount('/content/drive/')

cd drive/MyDrive/Assignments

import pandas as pd
from sklearn import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn import metrics

train_data=pd.read_csv("SalaryData_Test.csv")
train_data.sample(5)

train_data.isna().sum()

train_data.info()

train_data.duplicated().value_counts()

train_new_data=train_data.drop_duplicates()
train_new_data.sample(4)

train_data.isna().sum()

test_data=pd.read_csv("SalaryData_Train.csv")
test_data.head(5)

test_data.isna().sum().sum()

test_data.describe()

test_data.duplicated().value_counts()

test_new_data=test_data.drop_duplicates()
test_new_data.shape

x_train=train_new_data.iloc[:,:-1]
y_train=train_new_data.iloc[:,-1]
x_test=test_new_data.iloc[:,:-1]
y_test=test_new_data.iloc[:,-1]

encoder=preprocessing.LabelEncoder()
for i in x_train.columns:
  if x_train[i].dtype==object:
    x_train[i]=encoder.fit_transform(x_train[i])
  else:
    pass
for i in x_test.columns:
  if x_test[i].dtype==object:
    x_test[i]=encoder.fit_transform(x_test[i])
  else:
    pass

x_train

#normalizing
def std_val(val):
  x=val-val.min()/(val.max()-val.min())
  return x

x_train.head(5)

std_val(x_train)
std_val(x_test)

#Creating Navive Baise model
model=GaussianNB()

model=model.fit(x_train,y_train)

y_test_pred=model.predict(x_test)

metrics.accuracy_score(y_test,y_test_pred)

