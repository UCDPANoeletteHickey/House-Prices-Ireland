#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd #read CSV, data processing
import numpy as np # recommendation system
import matplotlib.pyplot as plt # data visualisation
import seaborn as sns # data visulisation

import warnings #to ignore warnings
warnings.filterwarnings("ignore") # no warnings will be printed from now on.


# In[13]:


df = pd.read_csv("Property_Price_Register_Ireland-28-05-2021.csv.zip")


# # DATA OVERVIEW

# In[14]:


df.info()
# 476745 entries, 9 columns
# data type for "IF_MARKET_PRICE" & "IF_VAT_EXCLUDED" is an integer
# data type for "SALE_PRICE" is a float
# can already see "POSTAL_CODE" & "PROPERTY_SIZE_DESC" have a large number of missing entries


# In[15]:


df.head()
#This will show the first 5 entries of the dataset 


# In[16]:


df.tail()
#shows the last 5 rows of the dataset
# "property_desc" shows if New Dwelling or Second Hand


# In[17]:


df.describe().transpose()
#From this we can see the average price in Ireland for a house is 260k


# In[18]:


df.sort_values("SALE_PRICE", ascending = False).head(5)
#shows most expensive houses sold in 2021 in Dublin


# In[19]:


df.sort_values("SALE_PRICE", ascending = False).tail(5)
#This shows the cheapest houses sold. Cheapest house sold in Cork 2019 for 5,000


# # Clean and Validate

# In[20]:


IrelandHouseprices_df = df.copy()
# make a copy of dataset


# In[21]:


IrelandHouseprices_df.info()
# "postal code" and "property_size_desc" have a large amount of data missing


# In[22]:


IrelandHouseprices_df.duplicated()
# not all values here a visible


# In[23]:


IrelandHouseprices_df.duplicated().sum()
# results are showing me that 763 are duplicated


# In[24]:


IrelandHouseprices_df.loc[IrelandHouseprices_df.duplicated(keep="first"),:]
# this will show me the rows that are duplicated expect for the first occurence 


# In[25]:


IrelandHouseprices_df.loc[IrelandHouseprices_df.duplicated(keep="last"),:]
# this code will show me the last duplicate occurence


# In[26]:


IrelandHouseprices_df.drop_duplicates().shape
#From review of both first and last rows these do seem true duplicates so using the drop function I will remove 
#the last occurence of the entry. 
#Results show that my rows have now reduce to 475982 from 476745


# In[27]:


IrelandHouseprices_df.isnull()
# Results show that there are true values reflecting missing values


# In[28]:


IrelandHouseprices_df.isnull().sum()
# Both postal_code and property_size_dec is missing. 
# For my analysis of prices and sales these columns are not required


# In[29]:


del IrelandHouseprices_df["POSTAL_CODE"]


# In[30]:


del IrelandHouseprices_df["PROPERTY_SIZE_DESC"]


# In[31]:


IrelandHouseprices_df.isnull().sum()
#cross check to see if any missing values still remain and we can see by results there is not


# In[32]:


IrelandHouseprices_df.shape
#Now we can see the columns have reduce to 7 as I have deleted both Postal Code and Property Size Desc


# In[33]:


IrelandHouseprices_df["SALE_DATE"] = pd.to_datetime(df["SALE_DATE"])


# In[34]:


IrelandHouseprices_df.dtypes
#Changing Sale date in to datetime to allow to carry out analysis of sale trends over the years


# In[35]:


IrelandHouseprices_df.sort_values(by="COUNTY")
#Sorting in alphabetic order


# In[36]:


IrelandHouseprices_df = IrelandHouseprices_df.rename(columns={"COUNTY":"County"})
IrelandHouseprices_df.head()
#Renaming "COUNTY" column to "County"


# In[37]:


Province = pd.read_excel("list-counties-ireland-433j.xlsx")
#Entering new dataset as I want to add an new column to existing dataset to include "Province"


# In[38]:


Province.info()
# 44 entries and 7 columns


# In[39]:


Province.head()
#Can see County and Province columns


# In[40]:


Province.columns


# In[41]:


Province2 = Province.drop(['SNo', 'Population', 'Rank','Change since'], axis=1)
# Removing unecessary columns


# In[42]:


Province2.head()


# In[43]:


HouseSales= pd.merge(IrelandHouseprices_df, Province2)
#Merging both datasets together to include the Province


# In[44]:


HouseSales.head()
# Can now see Province in the last column


# In[45]:


HouseSales.nunique()
#this will show the number of unique values in each column


# # EXPLORATORY DATA ANALYSIS
# 

# In[46]:


plt.figure(figsize=(6,3))
sns.distplot(HouseSales["SALE_PRICE"])
#Graph 1 : Distribution of Sale Price


# In[47]:


# What province has the highest house sales
#Graph 2
sns.set(style="darkgrid")
plt.title("House Sales By Province")
sns.countplot(x="Province", data = HouseSales)

#From Graph we can see Leinster is by far the area with the highest housesales


# In[48]:


County_sales = HouseSales.groupby("County").size()


# In[49]:


County_sales
# Group the amount of housessold in each county


# In[50]:


#Graph3: Shows the number of HouseSales in each County


plt.figure(figsize=(26,10))
sns.set(style="darkgrid")
ax= sns.countplot(y="County", data=HouseSales,palette=("Set3"), order=HouseSales["County"].value_counts().index[0:15])
plt.title("County Sales")
plt.show     

#The largest amount of house sales is in Dublin. 
# The second largest area for house sale is Corks as Irelands second largest city this is expected


# In[51]:


Property_Type=HouseSales["PROPERTY_DESC"].value_counts()
Property_Type


# In[52]:


#Graph4 : Shows the number of new houses vs Second Hand Dwellings
sns.set(style="darkgrid")
plt.title("New Dwelling v Second Hand-Dwelling")
ax = sns.countplot(y="PROPERTY_DESC", data=HouseSales)

# The number of houses sales that are Second Hand Dwellings is far exceeding the New Dwelling sales


# # HouseSales Trends in Each Province 

# In[53]:


HouseSales["Province"].value_counts()


# In[54]:


Lenister_df = HouseSales[(HouseSales["Province"] =="Leinster")]
Lenister_df.head()


# In[55]:


Munster_df = HouseSales[(HouseSales["Province"] =="Munster")]
Connacht_df = HouseSales[(HouseSales["Province"] =="Connacht")]
Ulster_df = HouseSales[(HouseSales["Province"] =="Ulster")]
#created a dataset for each province to analysie more closely trends in each


# In[56]:


sns.set(style="darkgrid")
sns.kdeplot(data=Lenister_df["SALE_DATE"], shade=True)
plt.title("Volume of Sales Lenister")
plt.show
#Graphn5


# In[57]:


sns.set(style="darkgrid")
sns.kdeplot(data=Munster_df["SALE_DATE"], shade=True)
plt.title("Volume of Sales Munster")
plt.show
#Graph6


# In[ ]:


# sns.set(style="darkgrid")
sns.kdeplot(data=Connacht_df["SALE_DATE"], shade=True)
plt.title("Volume of Sales Connacht")
plt.show
#Graph7


# In[ ]:


sns.set(style="darkgrid")
sns.kdeplot(data=Ulster_df["SALE_DATE"], shade=True)
plt.title("Volume of Sales Ulster")
plt.show
#Graph8


# # Housesale Price Trends from 2010-2021

# In[61]:


sns.set_theme(style="whitegrid")


# In[67]:


sns.set(rc={"figure.figsize":(12,10)})


# In[72]:


ax = sns.lineplot(x="SALE_DATE", y="SALE_PRICE", data=HouseSales, hue="Province", style="Province", ci=False, markers=True)Hou
#Graph 9: Comparison of House Price Trends for the past 10years


# # Breakdown of Price Trends by Province

# In[80]:


ax = sns.lineplot(x="SALE_DATE", y="SALE_PRICE", data=Lenister_df,ci=False, markers=True)
#Graph 10: Lenister Price Trend


# In[81]:


ax = sns.lineplot(x="SALE_DATE", y="SALE_PRICE", data=Munster_df, ci=False, markers=True)
#Graph 11: Price Trend for Mun.


# In[75]:


ax = sns.lineplot(x="SALE_DATE", y="SALE_PRICE", data=Connacht_df, ci=False, markers=True)
#Graph 12: Price Trend for Connacht


# In[79]:


ax = sns.lineplot(x="SALE_DATE", y="SALE_PRICE", data=Ulster_df, ci=False, markers=True)
#Graph 13 Price Trend for Ulster


# In[ ]:




