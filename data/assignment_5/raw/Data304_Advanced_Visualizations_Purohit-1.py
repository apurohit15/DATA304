#!/usr/bin/env python
# coding: utf-8

# Abhi Purohit
# Data 304
# Assignment 5

# In[50]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go

'''
Step 1: Filter and Prepare Data
1. Load both CSV files.
2. Filter course_pathways.csv to include only students in the CECS program majoring in:
Data science
Artificial intelligence
Cybersecurity
3. Split the CoursePath string into individual courses.
4. For each student, use course_catalog_by_major.csv to:
Identify the required courses for their major
Remove any electives from their course path
5. Retain only the ordered sequence of required courses
'''


# In[52]:


pathways = pd.read_csv("Assignment5_Purohit/course_pathways.csv")
pathways.head(5)


# In[54]:


catalog = pd.read_csv("Assignment5_Purohit/course_catalog_by_major.csv")
catalog.head(5)


# In[56]:


''' 
2. Filter course_pathways.csv to include only students in the CECS program majoring in:
Data science
Artificial intelligence
Cybersecurity 
'''


# In[58]:


cecs = ["Data science", "Artificial intelligence", "Cybersecurity"]
pathways = pathways[pathways['Major'].isin(cecs)]
pathways.head(5)


# In[60]:


pathways['Major'].value_counts()


# In[62]:


'''
3. Split the CoursePath string into individual courses.
In Python: str.split() , pandas.melt() , etc.
'''


# In[64]:


pathways['CoursePath'] = pathways['CoursePath'].str.split(" -> ")


# In[66]:


pathways.head()


# In[68]:


'''
4. For each student, use course_catalog_by_major.csv to:
Identify the required courses for their major
Remove any electives from their course path
'''


# In[70]:


required_courses = catalog[catalog['Type'] == 'Required']


# In[72]:


required_dict = required_courses.groupby("Major")["Course"].apply(list).to_dict()


# 5. Retain only the ordered sequence of required courses

# In[75]:


def filter_required_courses(row):
    major = row["Major"]
    course_list = row["CoursePath"]
    required_courses = required_dict.get(major, [])
    
    return [course for course in course_list if course in required_courses]


# In[77]:


pathways["RequiredCourseList"] = pathways.apply(filter_required_courses, axis=1)


# In[79]:


pathways.head()


# In[81]:


pathways['CoursePath'].value_counts()


# In[83]:


pathways['RequiredCourseList'].value_counts()


# In[85]:


'''
Step 2: Extract Transitions
For each student's required course sequence, extract consecutive transitions.
For example, the path: Intro to Python -> Data Wrangling -> Machine Learning
should yield the transitions:

Intro to Python → Data Wrangling
Data Wrangling → Machine Learning
Aggregate all transitions across all students. Count how many students made each
transition.
'''


# In[87]:


transitions = []

for course in range(len(pathways)):
    courses = pathways.iloc[course]["RequiredCourseList"]
        
    if len(courses) < 2:
        continue

    for index in range(len(courses) - 1):
        source = courses[index]
        target = courses[index + 1]
        transitions.append((source, target))


# In[89]:


count = {}

for transition in transitions:
    if transition in count:
        count[transition] += 1
    else:
        count[transition] = 1


# In[91]:


'''
Step 3: Create the Sankey Diagram
Using either R or Python:

Create a Sankey diagram using your aggregated transition data.
Nodes should be course titles.
Links should represent transitions with their frequency (weight).
Only include required courses (no electives).
The layout should flow from left to right.
Label your nodes clearly.
'''


# In[103]:


''' 
I referenced the 'advanced_visualizations.Rmd' R file provided in Github 
Also, I had to set the font size to 5 so that all course labels would fit without overlapping.  
'''

course_transitions = []

for (source, target), value in count.items():
    course_transitions.append({"source": source, "target": target, "value": value})

transitions_df = pd.DataFrame(course_transitions)

unique_courses = pd.unique(transitions_df[["source", "target"]].values.ravel())
courses_df = pd.DataFrame({"name": unique_courses})

transitions_df["IDsource"] = transitions_df["source"].apply(lambda x: courses_df[courses_df["name"] == x].index[0])
transitions_df["IDtarget"] = transitions_df["target"].apply(lambda x: courses_df [courses_df ["name"] == x].index[0])

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,             
        thickness=20,        
        label=courses_df ["name"].tolist(),
        line=dict(color="black", width=0.5)
    ),
    link=dict(
        source=transitions_df["IDsource"],
        target=transitions_df["IDtarget"],
        value=transitions_df["value"]
    )
)])

fig.update_layout(
    title_text="Sankey Diagram - Required Course Transitions",
    font_size=5,
    width=1100, 
    height=600
)
fig.show()


# In[ ]:





# In[ ]:





# In[ ]:




