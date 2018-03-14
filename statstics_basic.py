
# coding: utf-8

# In[1]:


import pandas as pd

movies = pd.read_csv("fandango_score_comparison.csv")


# In[2]:


movies.head()


# In[3]:


import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

movies["Metacritic_norm_round"].hist()


# In[4]:


movies["Fandango_Stars"].hist()


# In[5]:


FS_mean = movies["Fandango_Stars"].mean()
FS_median = movies["Fandango_Stars"].median()
FS_std = movies["Fandango_Stars"].std()


# In[6]:


MN_mean = movies["Metacritic_norm_round"].mean()
MN_median = movies["Metacritic_norm_round"].median()
MN_std = movies["Metacritic_norm_round"].std()
print(FS_mean,MN_mean)
print(FS_median,MN_median)
print(FS_std,MN_std)


# In[7]:


plt.scatter(movies["Fandango_Stars"],movies["Metacritic_norm_round"])


# In[8]:


movies["fm_diff"] = movies["Metacritic_norm_round"]-movies["Fandango_Stars"]


# In[9]:


import numpy as np
movies["fm_diff"] = movies["fm_diff"].apply(np.absolute)


# In[10]:


sorted = movies.sort_values(by = "fm_diff", ascending=False)
sorted.head()


# In[11]:


from scipy.stats import pearsonr
r, p = pearsonr(movies["Fandango_Stars"],movies["Metacritic_norm_round"])
print(r,p)


# In[12]:


from scipy.stats import linregress

slope, intercept, r_value, p_value, std_err = linregress(movies["Metacritic_norm_round"],movies["Fandango_Stars"])
pred_3 = 3*slope + intercept
print(pred_3)


# In[13]:


pred_1 = 1*slope + intercept
print(pred_1)


# In[14]:


pred_5 = 5*slope + intercept
print(pred_5)


# In[16]:


plt.scatter(movies["Metacritic_norm_round"],movies["Fandango_Stars"])
x = np.asarray([1,0,5.0])
y = slope*x+intercept
plt.plot(x,y)
plt.xlim(1,5)
plt.show()

