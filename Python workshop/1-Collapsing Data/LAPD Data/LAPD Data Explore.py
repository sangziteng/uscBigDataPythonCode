#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Declare Libraries ##

import pandas as pd
import numpy as np 
import os 
import matplotlib.pyplot as plt


# In[2]:


# Set working Directory ##

os.chdir('./Datasets/LAPD Data')


# In[3]:


ls


# In[4]:


# Read Data #

data = pd.read_csv("./arrest-data-from-2010-to-present.csv")


# In[5]:


# Explore #

data.head()


# In[6]:


# See Data Size / Shape #

data.shape


# In[7]:


# Find Number of each offense #

pd.pivot_table(data, index = "Charge Group Description", values = "Report ID", aggfunc = "count").sort_values("Report ID")


# In[8]:


data['Date'] = pd.to_datetime(data["Arrest Date"], errors = 'coerce').dt.year

GRAPH = pd.pivot_table(data, index = ["Charge Group Description", "Date"], values = "Report ID", aggfunc = "count").sort_values("Report ID")
GRAPH = GRAPH.reset_index()


# In[9]:


# Not a beautiful graph for a number of reasons # 

import seaborn as sns

p =sns.lineplot(data = GRAPH, x = "Date", y = "Report ID", hue = "Charge Group Description")

p.legend(ncol = 2, loc = 0, bbox_to_anchor=(1.05, -0.2))


# In[10]:


g = sns.FacetGrid(data = GRAPH.sort_values(by =["Charge Group Description", "Date"]), col = "Charge Group Description", col_wrap = 1, sharey = False)
g = g.map(plt.plot, "Date", "Report ID")
plt.show()

