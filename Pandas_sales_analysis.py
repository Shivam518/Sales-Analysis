#!/usr/bin/env python
# coding: utf-8

# In[23]:


#import importlib
#importlib.reload(my_module)
import imp
imp.reload(module)

import pandas as pd
import os


# Task-1 = merging all data in one single file

# In[47]:


df = pd.read_csv('F:\pandas\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data\Sales_April_2019.csv')


files = [file for file in os.listdir("F:\pandas\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data")]

all_month_data=pd.DataFrame()

for file in files:
    df=pd.read_csv("F:/pandas/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/"+file)
    all_month_data=pd.concat([all_month_data,df])
    
all_month_data.to_csv('F:\pandas\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data\Total_sales.csv',index=False)


# In[27]:


all_data=pd.read_csv('F:\pandas\Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data\Total_sales.csv')
all_data.head()


# Task_2 # to clean data

# In[33]:


nan_data=all_data[all_data.isna().any(axis=1)]
nan_data
all_data=all_data.dropna(how='all')
all_data


# Taske_3 - Find or and delete

# In[39]:


all_data=all_data[all_data['Order Date'].str[0:2]!='Or']
all_data


# Convert column into correct type

# In[42]:


all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered'])#make int
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])#make int
all_data.head()


# #creating custom column month for calclation

# Task_4 adding month column`

# In[37]:


all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')
all_data.head()


# Task_5 adding sales column

# In[43]:


all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# Task - 6: adding City column

# In[71]:


def get_city(address):
    return address.split(',')[1]

#what id same city in diffrecnt country
def get_state(address):
    return address.split(', ')[2].split(' ')[0]

all_data['City']=all_data['Purchase Address'].apply(lambda x:f'{get_city(x)} (  {get_state(x)})')
all_data.head()


# ### Question -1 What was best month of sale and How much we earned

# In[51]:


results=all_data.groupby('Month').sum()
results['Sales']


# In[59]:


import matplotlib.pyplot as plt
month=range(1,13)
plt.bar(month, results['Sales'])
plt.xticks(month)
plt.xlabel('Month In Number')
plt.ylabel('Sales in $')
plt.show()


# Qustion: Which city has max sales 

# In[73]:


results=all_data.groupby('City').sum()
results


# In[79]:


import matplotlib.pyplot as plt

#city=all_data['City'].unique() to make in order
city=[city for city , df in all_data.groupby('City')]

plt.bar(city, results['Sales'])
plt.xticks(city,rotation='vertical',size=8)
plt.xlabel('City')
plt.ylabel('Sales in $')
plt.show()


# ### Question3: What time we should advertise more to Maximize sell  product

# In[85]:


all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
all_data['Hour']=all_data['Order Date'].dt.hour
all_data.head()


# In[97]:


hour=[hour for hour,df in all_data.groupby(all_data['Hour'])]
plt.plot(hour,all_data.groupby(['Hour']).count())
plt.xticks(hour)
plt.xlabel('Hours')
plt.ylabel('Number of order')
plt.grid()
plt.show()
#all_data.groupby(['Hour']).count()


# #### Qustion-4: What product sold together?

# In[1]:


df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
df=df[['Order ID','Grouped']].drop_duplicates()
df.head(100)


# In[151]:


from itertools import combinations
from collections import Counter

count=Counter()

for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))#if we want to see 3 product put 3 instead 2
    
for key,value in count.most_common(10):
    print(key,value)


# #### Question : What product sold most and why you think it sold most?

# In[163]:


product_group=all_data.groupby('Product')
quatity_orderd=product_group.sum()['Quantity Ordered']
products=[product for product,df in product_group]
plt.bar(products,quatity_orderd)
plt.xlabel('Products')
plt.ylabel('Quantity Orders')
plt.xticks(products,rotation='vertical',size=8)
plt.show()


# In[172]:


prices=all_data.groupby('Product').mean()['Price Each']

fig,ax1=plt.subplots()

ax2=ax1.twinx()

ax1.bar(products,quatity_orderd,color='g')
ax2.plot(products,prices,'b-')

ax1.set_xlabel('Products')

ax1.set_xticklabels(products,rotation='vertical',size=8)

ax1.set_ylabel('Quantity Ordered',color='g')
ax2.set_ylabel('Prices',color='b')

plt.show()

