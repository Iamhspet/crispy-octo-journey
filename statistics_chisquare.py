
# coding: utf-8

# In[1]:


import pandas as pd
jeopardy = pd.read_csv("jeopardy.csv")
print(jeopardy.head())
print(jeopardy.columns)


# In[2]:


print(jeopardy.columns[0])


# In[3]:


print(len(jeopardy.columns))


# In[4]:


cols = jeopardy.columns.tolist()

for i in range(0,len(cols)):
    each = cols[i]
    if each[0] == " ":
        cols[i] = each[1:]
        
jeopardy.columns = cols
print(jeopardy.columns)
    


# In[5]:


def norm_str(string):
    temp = ""
    string = string.lower()
    letter = " abcdefghijklmnopqrstuvwxyz01234567890"
    for c in string:
        if c in letter:
            temp = temp + c
    return(temp)

        
            


# In[6]:


jeopardy["clean_question"] = jeopardy["Question"].apply(norm_str)
jeopardy["clean_answer"] = jeopardy["Answer"].apply(norm_str)


# In[7]:


jeopardy.head()


# In[8]:


def norm_value(string):
    temp = ""
    num = "0123456789"
    for c in string:
        if c in num:
            temp = temp + c
    try:
        val = int(temp)
    except:
        val = 0
    return val
jeopardy["clean_value"] = jeopardy["Value"].apply(norm_value)


# In[9]:


jeopardy["Air Date"] = jeopardy["Air Date"].apply(pd.to_datetime)


# In[10]:


def count_match(row):
    split_answer = row['clean_answer'].split(" ")
    split_question = row['clean_question'].split(" ")
    if "the" in split_answer:
        split_answer.remove("the")
    match_count = 0
    if len(split_answer) == 0:
        return 0
    else:
        for each in split_answer:
            if each in split_question:
                match_count = match_count + 1
        return (match_count / len(split_answer))


# In[11]:


jeopardy['answer_in_question'] = jeopardy.apply(count_match, axis = 1)
jeopardy.head()


# In[12]:


jeopardy["answer_in_question"].mean()


# In[13]:


question_overlap = []
terms_used = set()
for index, row in jeopardy.iterrows():
    split_question = row['clean_question'].split(" ")
    split_question = [q for q in split_question if len(q) >= 6]
      
    match_count = 0
    for each in split_question:
        if each in terms_used:
            match_count += 1
    for each in split_question:
        terms_used.add(each)
    if len(split_question) > 0 :
        match_count = match_count/len(split_question)
    question_overlap.append(match_count)
jeopardy['question_overlap'] = question_overlap
jeopardy['question_overlap'].mean()


# In[15]:



def high_low(row):
    if row['clean_value'] > 800:
        value = 1
    else:
        value = 0
    return value

jeopardy['high_value'] = jeopardy.apply(high_low,axis=1)
def high_low_count(word):
    low_count = 0
    high_count = 0
    for index, row in jeopardy.iterrows():
        split_question = row['clean_question'].split(" ")
        if word in split_question:
            if row['high_value'] == 1:
                high_count +=1
            else:
                low_count +=1
    return high_count, low_count
observed_expected = []
list_term_used = list(terms_used)
comparison_terms = list_term_used[:5]
for each in comparison_terms:
    observed_expected.append(high_low_count(each))
            
high_value_count = jeopardy[ jeopardy["high_value"] == 1 ].shape[0]
low_value_count = jeopardy[jeopardy["high_value"] == 0].shape[0]
print(high_value_count,low_value_count)


# In[18]:


chi_squared = []
from scipy.stats import chisquare
import numpy as np
for each in observed_expected:
    total = np.sum(each)
    total_prop = total/jeopardy.shape[0]
    expected_high_value_count = total_prop*high_value_count
    expected_low_value_count = total_prop*low_value_count
    observed = np.array([ each[0], each[1]])
    expected = np.array([expected_high_value_count, expected_low_value_count])
    chi_squared.append( chisquare(observed, expected))
chi_squared
    

