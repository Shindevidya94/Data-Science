# -*- coding: utf-8 -*-
"""Forecasting Airlines.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11wmlCsRzTGeMZudw2LXXCRuwUdrwnsgO
"""

from google.colab import files

files.upload()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import *
from math import sqrt

data=pd.read_excel('Airlines+Data.xlsx')
data

data.isna().sum().sum()

data.shape

#In times series problem alaways make the time column as index
data.set_index('Month',inplace=True)

"""Step 2 Visiualization of data"""

data.dtypes

data.shape

# We are going to use rolling avaergae to make data stationary with std deviation constant
# Here we are going to find rolling avarage for period of 12 months or yearly rolling avag and rolling std deviation
rollavg=data.rolling(window=12).mean()
rollstd=data.rolling(window=12).std()

# from graph below we can see the rolling avg is varying in between 130 to 330 or somthing and hence we need to do some data trandformation
# in above bwlow we can see there are spikes at some point which Shows data has seasonlaity and it also has trend as it is moving in
#upward direction. This means data is not stationary and we neeed to make data stationary in order to perform ARIMA
# https://www.youtube.com/watch?v=f6dwixb-4MM
original=plt.plot(data,label="Original",color="red")
rollavg=plt.plot(rollavg,label="Rolling Avg",color="blue")
rollstd=plt.plot(rollstd,label="Rolling Std",color="green")
plt.legend(loc='best')
plt.show()

#to make data stationary we use d key fuller test
from statsmodels.tsa.stattools import adfuller

# Now we doing Tetsing of Hypothesis using adfuller
# HO= Data is not stationary
# H1 = Data is stationary
# We are creating function to do TOH
def adfuller_test(Passangers):
  print('Dickey fuller test:')
  result=adfuller(Passangers)
  lables=['ADF Test Statstics','p-values','#Lags used','Number of Observations used']
  for value,label in zip(result,lables):
    print(label+' : '+str(value))

adfuller_test(data['Passengers'])

"""Data Transformation"""

# Logged data
data_log=np.log(data)
mvg_avg=data_log.rolling(window=12).mean()
mvg_std=data_log.rolling(window=12).std()
plt.plot(data_log)
plt.plot(mvg_avg)
plt.show()

# data_log diff
data_log_diff=data_log-mvg_avg
data_log_diff.dropna().head()

def stationary(timeseries):
  # Calsulating rolling mean and std deviation
  rollmean=timeseries.rolling(window=12).mean()
  rollstd=timeseries.rolling(window=12).std()
  #Plotting graph with orginal data, rollmean and rollstd
  plt.figure(figsize=(10,7))
  original=plt.plot(timeseries,color='red',label="Orginal")
  mean_roll=plt.plot(rollmean,color='blue',label='Rolling mean')
  std_roll=plt.plot(rollstd,color='green',label='Rolling std')
  plt.show(block=False)
  #Dickley Fuller test
  print('Dicky Fuller test')
  result=adfuller(timeseries['Passengers'])
  lables=['ADF Test Statstics','p-values','#Lags used','Number of Observations used']
  for value,label in zip(result,lables):
    print(label+' : '+str(value))

stationary(data_log_diff.dropna())

# Exponential data transformation with exponentially weighted moving average
data_exp=data_log.ewm(halflife=12,min_periods=0,adjust=True).mean()
data_exp_diff=data_log-data_exp

stationary(data_exp_diff)

from statsmodels.tsa.seasonal import seasonal_decompose
decomp=seasonal_decompose(data_log)
trend=decomp.trend
seasonal=decomp.seasonal
residual=decomp.resid
decomp_data=residual
decomp_data=decomp_data.dropna()
stationary(decomp_data)

result=adfuller(decomp_data)
lables=['ADF Test Statstics','p-values','#Lags used','Number of Observations used']
for value,label in zip(result,lables):
  print(label+' : '+str(value))

data_shift=data_log-data_log.shift()
data_shift=data_shift.dropna()
stationary(data_shift)

# we are going to find p,q,d values to run for ARIMA
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

lag_acf=acf(data_shift,nlags=20)
lag_pacf=pacf(data_shift,nlags=20)

plt.figure(figsize=(20,10))
plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='green')
plt.axhline(y=-1.96/np.sqrt(len(data_shift)),linestyle='--',color='green')
plt.axhline(y=1.96/np.sqrt(len(data_shift)),linestyle='--',color='green')
plt.title('Autocorrelation Function')

plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='green')
plt.axhline(y=-1.96/np.sqrt(len(data_shift)),linestyle='--',color='green')
plt.axhline(y=1.96/np.sqrt(len(data_shift)),linestyle='--',color='green')
plt.title('Autocorrelation Function')

# from above graph we can fing q and p value to run ARIMA model.
# from 1st graph we can get q value and it where out graph is cutting 0 line and it is aroung 2
# from 2nd graph we can get q value which is also around 2
# and d will be be between 1 and 2
from statsmodels.tsa.arima_model import ARIMA
from sklearn.model_selection import train_test_split

data_shift.dropna()

model1 = ARIMA(data_shift, order=(2,1,0))
results_AR = model1.fit(disp=-1)
# plt.plot(airpass_log_diff)
# plt.plot(results_AR.fittedvalues, color='red')
# plt.title('RSS: %.4f'%sum((results_AR.fittedvalues - airpass_log_diff['Passengers'])**2))
# print('Plotting AR model')

import statsmodels.api as sm

model = sm.tsa.arima.ARIMA(data_shift, order=(1,1,2))
result = model.fit()

from statsmodels.tsa.arima.model import ARIMA

plt.figure(figsize=(20,10))
model=ARIMA(data_log, order=(2,1,2))
results=model.fit()
plt.plot(data_shift)
plt.plot(results.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results.fittedvalues-data_shift['Passengers'])**2))
print('plotting ARIMA model')

predictions=pd.Series(results.fittedvalues, copy=True)
print(predictions.head())

predictions_cum_sum=predictions.cumsum()
print(predictions_cum_sum.head())

predictions_log=pd.Series(data_log['Passengers'])
predictions_log=predictions_log.add(predictions_cum_sum,fill_value=0)
predictions_log.head()

predictions_ARIMA=np.exp(pd.Series(data_log['Passengers']))
plt.figure(figsize=(20,10))
plt.plot(data)
plt.plot(predictions_ARIMA)

results.forecast(steps=120)

