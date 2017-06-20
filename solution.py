
# coding: utf-8

# ### Election Data Analysis

# In[1]:

# Project description: 2012 election analysis, political polls for candidates, donors, etc.


# In[2]:

# questions to ask:
# 1. Who were polled? What were their party affiliations?
# 2. Did the poll results favor Obama or Romney?
# 3. How did the undecided voters affect the poll? Can we account for them?
# 4. How did the voter sentiment change over time?
# 5. Did the debates indeed have an impact on the polls?


# In[1]:

import numpy as np


# In[2]:

import pandas as pd


# In[3]:

from pandas import Series, DataFrame


# In[4]:

import matplotlib.pyplot as plt


# In[5]:

import seaborn as sns


# In[6]:

sns.set_style('whitegrid')


# In[7]:

get_ipython().magic(u'matplotlib inline')


# In[8]:

from __future__ import division


# In[11]:

# data source: HuffPost Pollster


# In[12]:

# use the requests module to get some of the data from the web


# In[13]:

# use StringIO to work with the csv file


# In[10]:

import requests


# In[11]:

from StringIO import StringIO


# In[12]:

# the url for the poll data csv
url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"


# In[13]:

# use requests to get the data in text form
source = requests.get(url).text


# In[14]:

source


# In[15]:

# use StringIO to avoid I/O error with pandas
poll_data = StringIO(source)


# In[16]:

# after we have the data, we import it as dataframe
poll_df = pd.read_csv(poll_data)


# In[17]:

poll_df.info()


# In[18]:

poll_df.describe()


# In[19]:

poll_df.head()


# In[20]:

# get a sense on number of observations
sns.factorplot('Number of Observations', data = poll_df)


# In[21]:

poll_df['Number of Observations'].hist()


# In[22]:

# get a sense of population
sns.factorplot('Population', data = poll_df, kind = 'count', aspect = 2)


# In[23]:

# get a sense of mode
sns.factorplot('Mode', data = poll_df, kind = 'count', aspect = 2)


# In[24]:

# get a sense of partisan
sns.factorplot('Partisan', data = poll_df, kind = 'count', aspect = 2)


# In[42]:

# partisan: 强烈支持者  nonpartisan: 无党派的  pollster: 民意测验者


# In[25]:

# get a sense of affiliation
sns.factorplot('Affiliation', data = poll_df, kind = 'count', aspect = 2)


# In[44]:

# further sort the affiliation by population using "hue"


# In[26]:

sns.factorplot('Affiliation', data = poll_df, hue = 'Population', kind = 'count', aspect = 2)


# In[46]:

# it looks like that we get a strong showing of likely and registered voters, meaning the polls would be a good reflection


# In[27]:

# Now let's look at Romney, Obama, and the Undecided data
# get the average
avg = pd.DataFrame(poll_df.mean())


# In[28]:

avg


# In[29]:

# remove number of observation data
avg.drop('Number of Observations', axis = 0, inplace = True)


# In[30]:

avg.drop('Question Text', axis = 0, inplace = True)


# In[31]:

avg.drop('Question Iteration', axis = 0, inplace = True)


# In[32]:

avg.drop('Other', axis = 0, inplace = True)


# In[33]:

avg


# In[34]:

# get the standard deviation
std = pd.DataFrame(poll_df.std())


# In[35]:

std.drop('Other', axis = 0, inplace = True)


# In[36]:

std.drop('Question Text', axis = 0, inplace = True)


# In[37]:

std.drop('Question Iteration', axis = 0, inplace = True)


# In[38]:

std.drop('Number of Observations', axis = 0, inplace = True)


# In[39]:

std


# In[40]:

avg.plot(yerr = std, kind = 'bar', legend = False)


# In[90]:

# considering the undecided, Obama and Romney are really close


# In[91]:

# concatenate avg and std dataframes


# In[41]:

poll_avg = pd.concat([avg, std], axis = 1)

poll_avg.columns = ['Average', 'Standard Deviation']

poll_avg


# In[42]:

poll_df.head()


# In[98]:

# do a quick time series analysis using the end date of polls


# In[43]:

poll_df.plot(x='End Date', y = ['Obama', 'Romney', 'Undecided'], marker = 'o', linestyle = '-')


# In[44]:

# another way to plot sentiment vs. time 
# for timestamps
from datetime import datetime


# In[45]:

# add a new column to check the difference between Obama and Romney
poll_df['Difference']=(poll_df.Obama - poll_df.Romney)/100


# In[46]:

poll_df.head()


# In[47]:

# group the polls by their start date using groupby
poll_df2 = poll_df.groupby(['Start Date'], as_index = False).mean()


# In[110]:

poll_df2


# In[48]:

poll_df2.tail(100)


# In[49]:

# plot the difference
fig = poll_df2.plot('Start Date', 'Difference', figsize = (10,4), marker = 'o', linestyle = '-', color = 'green')


# In[113]:

# zoom in and check the situations of difference on the three debate dates: 10/3/2012, 10/11/2012, 10/22/2012


# In[114]:

# plot some lines as markers


# In[115]:

# In order to find where to set the x limits for the figure we need to find out where the index for the month of October in 2012 is.


# In[50]:

# Set row count and xlimit list
row_index = 0
xlimit = []

# Cycle through dates until 2012-10 is found, then print row index
for date in poll_df2['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_index)
        row_index +=1
    else:
        row_index += 1
        
print min(xlimit)
print max(xlimit)


# In[51]:

# Start with original figure
fig2 = poll_df2.plot('Start Date','Difference',figsize=(10,4),marker='o',linestyle='-',color='green',xlim=(325,352))

# Now add the debate markers
plt.axvline(x=327, linewidth=4, color='grey')
plt.axvline(x=335, linewidth=4, color='grey')
plt.axvline(x=343, linewidth=4, color='grey')


# ### Donor Data Set Analysis

# In[1]:

# import the donor data set to see where the donations were from and how they affect the campaign. 


# In[2]:

# the questions to answer:
# 1.) How much was donated and what was the average donation?
# 2.) How did the donations differ between candidates?
# 3.) How did the donations differ between Democrats and Republicans?
# 4.) What were the demographics of the donors?
# 5.) Is there a pattern to donation amounts?


# In[3]:

# Read in the dataset as a dataframe first


# In[52]:

donor_df = pd.read_csv('Election_Donor_Data.csv')


# In[53]:

# get a quick overview
donor_df.info()


# In[17]:

# this dataset has more than 1 million rows, VERY BIG dataset!


# In[54]:

# get a closer overview
donor_df.head(5)


# In[20]:

# We see information on candidates, contributors' names, contributors' cities, contributors' zip codes, 
# their employers, occupations, donation amounts, donation dates, etc. 


# In[55]:

# since we care most about the donation amounts, let's do some analysis on that
donor_df['contb_receipt_amt'].value_counts()


# In[22]:

# there were 8079 different donor amounts!!


# In[56]:

# let's calculate the mean and standard deviation of the donations
don_mean = donor_df['contb_receipt_amt'].mean()


# In[57]:

don_mean


# In[58]:

don_std = donor_df['contb_receipt_amt'].std()


# In[59]:

don_std


# In[60]:

print 'the average donation amount was %.2f with a std of %.2f'%(don_mean, don_std) 


# In[29]:

# we see small mean and huge standard deviation


# In[61]:

top_donor = donor_df['contb_receipt_amt'].copy()


# In[31]:

top_donor


# In[62]:

top_donor.sort_values() 


# In[63]:

top_donor.value_counts()


# In[36]:

# most people donated $100 and whole numbers, much more than decimal points 


# In[37]:

# get rid of the negative donation amounts


# In[64]:

top_donor = top_donor[top_donor > 0] 


# In[65]:

top_donor


# In[40]:

# most people made donations for amounts under 3000, let's make a histogram to see where donations concentrate


# In[66]:

pop_don = top_donor[top_donor < 3000]


# In[67]:

pop_don


# In[68]:

pop_don.hist(bins = 100, color = 'green')


# In[69]:

donor_df.head()


# In[70]:

# let's look into the donations by candidates


# In[71]:

candidates = donor_df['cand_nm'].unique()


# In[72]:

candidates


# In[73]:

# check the party affiliations
party_map = {'Bachmann, Michelle':'Republican', 
             'Romney, Mitt': 'Republican', 
             'Obama, Barack':'Democrat',
       "Roemer, Charles E. 'Buddy' III":'Republican', 
             'Pawlenty, Timothy': 'Republican',
       'Johnson, Gary Earl': 'Republican', 
             'Paul, Ron': 'Republican', 
             'Santorum, Rick': 'Republican', 
             'Cain, Herman':'Republican',
       'Gingrich, Newt':'Republican', 
             'McCotter, Thaddeus G':'Republican', 
             'Huntsman, Jon':'Republican',
       'Perry, Rick':'Republican'}


# In[74]:

party_map


# In[75]:

# map the party with candidates
donor_df['Party']=donor_df.cand_nm.map(party_map)


# In[76]:

donor_df.head()


# In[77]:

# clean the donor_df dataframe by removing those entries with refunds, i.e., donation < 0


# In[78]:

donor_df=donor_df[donor_df.contb_receipt_dt > 0]


# In[79]:

# let's check the donation data grouped by each candidate


# In[80]:

donor_df.groupby('cand_nm').count()


# In[81]:

donor_df.groupby('cand_nm')['contb_receipt_amt'].count()


# In[82]:

# Obama has the most number of donations among the candidates


# In[83]:

# now let's compare the total amounts of donations for each candidate


# In[84]:

donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()


# In[85]:

# Obama also leads in terms of the sum amount of donations


# In[86]:

# just make it read a little better


# In[87]:

cand_don = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()


# In[88]:

cand_don # a Series


# In[89]:

cand_don.index[0]


# In[90]:

cand_don.index[4]


# In[92]:

counter = 0

for don in cand_don:
    print 'The candidate %s raised %.0f dollars of donations.' %(cand_don.index[counter], don)
    print '\n'
    counter += 1


# In[93]:

# plot it to visualize the difference in donations among candidates


# In[96]:

cand_don.plot(kind = 'bar', color = 'seagreen')


# In[97]:

# how about total donations of Democrats vs. Republican?


# In[99]:

donor_df.groupby('Party')


# In[100]:

donor_df


# In[102]:

donor_df.groupby('Party')['contb_receipt_amt'].sum()


# In[103]:

# plot it up


# In[104]:

donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind = 'bar', color = 'purple')


# In[105]:

# look further into who the donors are (their occupation)


# In[106]:

donor_df.groupby('contbr_occupation')['contb_receipt_amt'].sum()


# In[107]:

donor_df.pivot_table('contb_receipt_amt', index = 'contbr_occupation', columns = 'Party', aggfunc = 'sum')


# In[108]:

occupation_df = donor_df.pivot_table('contb_receipt_amt', index = 'contbr_occupation', columns = 'Party', aggfunc = 'sum')


# In[110]:

occupation_df.info()


# In[112]:

occupation_df.shape


# In[114]:

#  small donations of 20 dollars by one type of occupation won't give us too much insight. Do some cut-off.


# In[117]:

occupation_df=occupation_df[occupation_df.sum(1) > 1000000]


# In[118]:

occupation_df


# In[119]:

occupation_df.shape


# In[120]:

# plot it up
occupation_df.plot(kind= 'bar')


# In[121]:

# retired people made the most donations


# In[122]:

# not quite readable, switch the plot in the horizontal direction


# In[123]:

occupation_df.plot(kind= 'barh', figsize = (12,12), cmap = 'seismic')


# In[124]:

occupation_df.plot(kind= 'barh', figsize = (12,12))


# In[125]:

# drop the invalid occupations:


# In[126]:

occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS', 'INFORMATION REQUESTED'], axis = 0,  inplace = True)


# In[127]:

occupation_df.plot(kind= 'barh', figsize = (12,12))


# In[128]:

# CEO and C.E.O. are the same and need to be combined


# In[130]:

# Set new ceo row as sum of the current two
occupation_df.loc['CEO']=occupation_df.loc['CEO'] + occupation_df.loc['C.E.O.']


# In[131]:

occupation_df.drop(['C.E.O.'], inplace = True)


# In[132]:

occupation_df


# In[133]:

# the plot can be refined and finalized.


# In[134]:

occupation_df.plot(kind= 'barh', figsize = (12,12))


# In[ ]:



