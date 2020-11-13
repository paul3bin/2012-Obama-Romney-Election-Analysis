from __future__ import division
import pandas as pd
from pandas import DataFrame,Series
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
sns.set_style('whitegrid')
import requests#to pull http requests
from io import StringIO

#Election Data Project - Polls and Donors


#Questions
"""
1.  Who was being polled and what was their party affiliation
2.  Did poll results favor Romney or Obama?
3.  How do undecided voters affect the poll?
4.  Can we account for the undecided voters?
5.  How did voter sentiment change over time?
6.  Can we see an effect in the polls from the debates?
"""

#Part 1

#Url given below the source of data
#http://elections.huffingtonpost.com/pollster
#http://docs.python-requests.org/en/latest

url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"

source = requests.get(url).text#this line gets the data from the url and converts it into text format
poll_data = StringIO(source)#converting the text data into a string data
poll_df = pd.read_csv(poll_data)#passing the data from the poll_data to a dataframe
print(poll_df.info())
print(poll_df.head())

poll = pd.DataFrame(poll_df['Affiliation'].value_counts())
poll.reset_index(inplace=True)
poll = poll.rename(columns={'index':'Affiliation','Affiliation':'Count'})
print(poll)
sns.barplot(x='Affiliation',y='Count',data=poll)
plt.show()
poll_new = pd.DataFrame(poll_df[['Population','Affiliation']])
poll_aff = poll_new['Population'].value_counts()
print(poll_aff)
#print(poll_new)
#sns.barplot(x='Affiliation',data=poll_new,hue='Population')
#plt.show()
avg = pd.DataFrame(poll_df.mean())
avg.drop('Number of Observations',axis=0,inplace=True)
print(avg.head())
std = pd.DataFrame(poll_df.std())
std.drop('Number of Observations',axis=0,inplace=True)
print(std.head())
avg.plot(yerr=std,kind='bar',legend=False)
plt.show()

poll_avg = pd.concat([avg,std],axis=1)
poll_avg.columns = ['Average','STD']
print(poll_avg)

#Part 2

poll_df.plot(x='End Date',y=['Obama','Romney','Undecided'],linestyle='',marker='o')
plt.show()

from datetime import datetime
poll_df['Difference'] = (poll_df['Obama']-poll_df['Romney'])/100
poll_df = poll_df.groupby(['Start Date'],as_index=False).mean()
print(poll_df.head())

poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple')
plt.show()

row_in = 0
xlimit = []

for date in poll_df['Start Date']:
    if date[0:7]=='2012-10':
        xlimit.append(row_in)
        row_in+=1
    else:
        row_in+=1
print(min(xlimit))
print(max(xlimit))

poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple',xlim=(325,352))
plt.axvline(x=325+2,linewidth=4,color='grey')
plt.axvline(x=325+10,linewidth=4,color='grey')
plt.axvline(x=325+21,linewidth=4,color='grey')
plt.show()

#Part 3

#Part 4