# -*- coding: utf-8 -*-
"""NLP Forestfire.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FGwvkNUMxmRw_YzNjQRx1VSN7xtQSRD1
"""

from google.colab import files

files.upload()

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from keras.layers import Dense

data=pd.read_csv('forestfires.csv')
data.head(5)

data.shape

data.drop(['month','day'],axis=1,inplace=True)

mapping = {'small': 1, 'large': 2}

data = data.replace(mapping)

x = np.array(data.iloc[:,0:28])
y = np.array(data.iloc[:,28])

def norm_func(i):
    x = (i-i.min())/(i.max()-i.min())
    return (x)

x_norm = norm_func(x)

x_train,x_test,y_train,y_test= train_test_split(x_norm,y, test_size=0.2,stratify = y)

model = Sequential()
model.add(Dense(8, input_dim=28, activation='linear'))
model.add(Dense(4,  activation='tanh'))
model.add(Dense(1,  activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history=model.fit(x_train, y_train, validation_split=0.3, epochs=120, batch_size=10)

scores = model.evaluate(x_train, y_train)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

scores = model.evaluate(x_test, y_test)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

