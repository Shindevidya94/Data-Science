# -*- coding: utf-8 -*-
"""TextMining Elons tweets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nWuy-kHk98XpIpWOrC0g8qXI67_ad8fq
"""

from google.colab import drive

drive.mount('/content/drive')

cd drive/MyDrive/Assignments

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from textblob import TextBlob
from wordcloud import WordCloud

data=pd.read_csv('Elon_musk.csv',encoding='latin1')
data

data.shape

#creating function to clean text

def clean_txt(text):
  text=re.sub(r'@[A-Za-z0-9]+','',text)          #removes @mention
  text=re.sub(r'#','',text)
  text=re.sub(r'RT[\S]+','',text)
  text=re.sub(r'https?:\/\/\S+','',text)
  return text

#cleaning text
data['Text']=data['Text'].apply(clean_txt)

#printing cleaned text
data

#Subjectivity - talks about as how text is subjective or how opinion oriented it is
#Polairy -  talks as how positive or negative text is

# creating function to get subjectivity
def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

# Creating function to get polarity
def getpolrity(text):
  return TextBlob(text).sentiment.polarity

# Creating new columns of polarity and subjectivity in data
data['Subjectivity']=data['Text'].apply(getSubjectivity)
data['Polarity']=data['Text'].apply(getpolrity)

data.sample(10)

# Will now analyze how well the sentiments are distributed that is done by finding out the common words. This is done
# applying Word cloud which is visulization method
#Plotting sentiment with Wordcloud
allwords=' '.join([text for text in data['Text']])
wordcloud=WordCloud(width=500,height=300,random_state=40,max_font_size=120).generate(allwords)
plt.imshow(wordcloud,interpolation="bilinear")
plt.axis('off')
plt.show

# Anlayising the polarity column of data by naming emtion as +ve,-ve or neutral
def getAnalysis(score):
  if score<0:
    return 'Negative'
  elif score==0:
    return 'Neutral'
  else:
    return 'Positive'

data['Analysis']=data['Polarity'].apply(getAnalysis)

data.sample(10)

#Plotting Subjectivity and Polariyity
plt.figure(figsize=(8,6))
plt.style.use('seaborn-darkgrid')
for i in range(0,data.shape[0]):
  plt.scatter(data['Polarity'][i],data['Subjectivity'][i],color='red')
plt.title('Sentiment Analysis')
plt.xlabel('Ploarity')
plt.ylabel('Subjectivity')
plt.show()

#getting percentage of postive tweets
ptweets=data[data.Analysis=='Positive']
ptweets=ptweets['Text']
round((ptweets.shape[0]/data.shape[0]*100),1)

ntweets=data[data.Analysis=='Negative']
ntweets=ntweets['Text']
round((ntweets.shape[0]/data.shape[0]*100),1)

neutraltweets=data[data.Analysis=='Neutral']
neutraltweets=neutraltweets['Text']
round((neutraltweets.shape[0]/data.shape[0]*100),1)

#value counts
data['Analysis'].value_counts()

#Plotting the analysis
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
data['Analysis'].value_counts().plot(kind='bar')
plt.show

