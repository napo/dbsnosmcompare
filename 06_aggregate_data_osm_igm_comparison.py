#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
pd.options.mode.chained_assignment = None
source_dir = "download"
start_dir = os.getcwd()
dest_dir = "data"
#06_aggregate_data_osm_igm_comparison.py


# In[3]:


# search all files inside a specific folder
# *.* means file name with any extension
os.chdir(source_dir)
dir_path = r'*.parquet'
data_files = glob.glob(dir_path)
datafiles = []
for f in data_files:
    if (f.find("_dbsn") == -1):
        datafiles.append(pd.read_parquet(f))
data_igm_osm = pd.concat(datafiles)
data_igm_osm = data_igm_osm.fillna(0).reset_index()
del data_igm_osm['index']
columns = data_igm_osm.columns.unique()


# In[4]:


# conversion in km
data_igm_osm.area_igm_buildings = data_igm_osm.area_igm_buildings / 1000
data_igm_osm.osm_in_igm_streets_length = data_igm_osm.osm_in_igm_streets_length / 1000
data_igm_osm.area_igm_buildings = data_igm_osm.area_igm_buildings / 1000
data_igm_osm.area_osm_buildings = data_igm_osm.area_osm_buildings / 1000
data_igm_osm.osm_streets_length = data_igm_osm.osm_streets_length / 1000
data_igm_osm.igm_streets_length = data_igm_osm.igm_streets_length / 1000
data_igm_osm.area_osm_in_igm_buildings = data_igm_osm.area_osm_in_igm_buildings / 1000
data_igm_osm.osm_in_igm_streets_length = data_igm_osm.osm_in_igm_streets_length / 1000


# In[5]:


df1 = data_igm_osm.groupby("region")['area_igm_buildings'].sum().to_frame().reset_index()
df2 = data_igm_osm.groupby("region")['area_osm_buildings'].sum().to_frame().reset_index()
df3 = data_igm_osm.groupby("region")['area_osm_in_igm_buildings'].sum().to_frame().reset_index()


# In[6]:


df4 = data_igm_osm.groupby("region")['igm_streets_length'].sum().to_frame().reset_index()
df5 = data_igm_osm.groupby("region")['osm_streets_length'].sum().to_frame().reset_index()
df6 = data_igm_osm.groupby("region")['osm_in_igm_streets_length'].sum().to_frame().reset_index()


# In[7]:


regions = df1.merge(df2).merge(df3).merge(df4).merge(df5).merge(df6)


# In[9]:


regions.to_csv(start_dir + os.sep + dest_dir + os.sep + "regions_osm_igm_comparison.csv",index=False)


# In[10]:


data_igm_osm.to_csv(start_dir + os.sep + dest_dir + os.sep + "provinces_osm_igm_comparison.csv",index=False)

