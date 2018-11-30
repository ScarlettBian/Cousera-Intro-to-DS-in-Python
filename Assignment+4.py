
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[60]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[61]:

Uttxt=pd.read_table('university_towns.txt', header=None)
print(Uttxt.iloc[0][0].split('(')[0])
print(type(Uttxt.iloc[0]))
print(type(Uttxt))
print(Uttxt)

df_Utowns = pd.DataFrame(columns=['State', 'RegionName'])


# In[62]:

j=0
for i in range(len(Uttxt)):
    if Uttxt.iloc[i].str.contains('[edit]', regex=False).bool():
        state=Uttxt.iloc[i][0].replace('[edit]', '')
    else:
        region=Uttxt.iloc[i][0].split(' (')[0]
        df_Utowns.loc[j]=[state, region]
        j+=1
print(df_Utowns)
print(len(df_Utowns['State'].unique()))
print(Uttxt[0].str.contains('[edit]', regex=False).sum())


# In[63]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
        
    return df_Utowns


# In[64]:

df_gdp=pd.read_excel('gdplev.xls', skiprows=219, usecols=[4, 6])
df_gdp.columns=['Quarterly', 'GDP']
df_gdp=df_gdp.set_index('Quarterly')
print(df_gdp.iloc[20:])


# In[65]:

df_recession=pd.DataFrame(columns=['start', 'bottom', 'end'])

start=None
bottom=None
end=None
i=0
k=0
while i<(len(df_gdp)-2):
    print('i',i, '  start', start, bottom, end)
    if start==None:
        # find the start of recession
        if df_gdp.iloc[i][0]>df_gdp.iloc[i+1][0] and df_gdp.iloc[i+1][0]>df_gdp.iloc[i+2][0] :
            start=df_gdp.iloc[[i]].index[0]
            i+=2
        else:
            i+=1
    else:
        # recession already started, find the end of the recession
        if i<(len(df_gdp)-2) and df_gdp.iloc[i][0]<df_gdp.iloc[i+1][0] and df_gdp.iloc[i+1][0]<df_gdp.iloc[i+2][0] :
            #while i<(len(df_gdp)-2) and df_gdp.iloc[i][0]<df_gdp.iloc[i+1][0] and df_gdp.iloc[i+1][0]<df_gdp.iloc[i+2][0] :
            
            end=df_gdp.iloc[[i+2]].index[0]            
            bottom=df_gdp.loc[start:end].idxmin()[0]
            # print([start, bottom, end])
            df_recession.loc[k]=[start, bottom, end]
            
            start=None
            bottom=None
            end=None
            k+=1
            i+=2
        else:
            i+=1

print(df_recession)


# In[66]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    return df_recession['start'][0] # 2008q2  2009q2  2009q4


# In[67]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
       
    return df_recession['end'][0] # 2008q2  2009q2  2009q4


# In[68]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    return df_recession['bottom'][0] # 2008q2  2009q2  2009q4


# In[69]:

df_house = pd.read_csv('City_Zhvi_AllHomes.csv')
print(df_house)
df_house.columns[(-16*12-8):]


# In[70]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[71]:

df_houses = (df_house.iloc[:,(-16*12-8):].groupby(pd.PeriodIndex(df_house.iloc[:,(-16*12-8):].columns, freq='Q'), axis=1)
             .mean()
             .rename(columns=lambda c: str(c).lower()))

df_houses['State']=df_house['State']
df_houses['RegionName']=df_house['RegionName']

df_houses['State']=df_houses['State'].map(states)

df_houses=df_houses.set_index(['State', 'RegionName'])

print(df_houses)


# In[72]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    return df_houses


# In[73]:

df_ttest=df_houses[[get_recession_start(), get_recession_bottom(), get_recession_end()]]

df_ttest['ratio']=df_ttest[get_recession_start()]/df_ttest[get_recession_bottom()]
print(df_ttest.head())
df_ttest=df_ttest['ratio']

print(type(df_ttest))
df_ttest=df_ttest.reset_index()
print(type(df_ttest))
print(df_ttest) # [10730 rows x 3 columns]
print(df_Utowns) # [517 rows x 2 columns]


# In[74]:

row=df_ttest.iloc[23,0:2]
utowns=df_Utowns.copy()
utowns['row1']=row[0]
utowns['row2']=row[1]
row2=utowns.iloc[-8,0:2]

print(type(row))
print(df_Utowns.head())
print(utowns.head())

print(row[1])
print(row2[1])
print(len(row[1]))
print(len(row2[1]))

print(row[1] == row2[1])

print(row==['Wisconsin', 'Milwaukee'])


x=lambda row1, row2: sum(row1==row2)
x(row, row2)


# In[75]:

def town_in_university_towns(utowns):
    x=utowns.apply(lambda row: row[0]==row[2] and row[1]==row[3] , axis=1)
    if sum(x)==0: return 0
    else:return 1

town_in_university_towns(utowns)


# In[76]:

df_ttest['Utown']=0
for i in range(len(df_ttest)):
    row=df_ttest.iloc[i][['State', 'RegionName']]
    utowns=df_Utowns.copy()
    utowns['row1']=row[0]
    utowns['row2']=row[1]
    df_ttest['Utown'][i]=town_in_university_towns(utowns)


# In[77]:

#df_ttest['Utown']=0

#%for i in range(len(df_ttest)):
#    house=df_ttest.iloc[i][['State', 'RegionName']]
#    for j in range(len(df_Utowns)):
#        utown=df_Utowns.iloc[j][['State', 'RegionName']]
#        
#        if sum(house==utown)==2:
#            df_ttest['Utown'][i]=1

#print(df_ttest['Utown'])


# In[78]:

print(sum(df_ttest['Utown']))
print(df_ttest)


# In[89]:

df_Ut=df_ttest[df_ttest['Utown']==1]['ratio'].dropna()
df_Nt=df_ttest[df_ttest['Utown']==0]['ratio'].dropna()
print(len(df_Ut), len(df_Nt))  # 269 10461  # 257 9599
#print(df_Ut, df_Nt)
result=ttest_ind(df_Ut, df_Nt)[1]

#results=ttest_ind(df_Ut,df_Nt)[2]


# In[90]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    better="university town"
    if df_Ut.mean()>df_Nt.mean(): better="non-university twon"
    
    pval=0.01
    if result <= pval: return ["True",  result, better]
    if result > pval: return ["False", result, better]
run_ttest()

