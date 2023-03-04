#!/usr/bin/env python
# coding: utf-8

# In[6]:


import geopandas as gpd
import os
import fiona
import matplotlib.pyplot as plt
import pandas as pd
import re
source_dir = "download"
start_dir = os.getcwd()


# In[7]:


dir_list = os.listdir(source_dir)
provincies = [f.replace("_dbsn.gdb", "") for f in dir_list if "_dbsn.gdb" in f]


# In[16]:


for province in provincies:
     print(province)
     dfdata = []
     filename = province + "_dbsn.gdb"
     igm_layers_list = fiona.listlayers(filename)
     for l in igm_layers_list:
          fdata = {}
          data = gpd.read_file(filename,layer=l)
          fdata['name'] = l
          fdata['objects'] = data.shape[0]
          data['meta_ist'] = data['meta_ist'].fillna("zero")
          osm_objects = 0
          sources = data.meta_ist.unique()
          regex = re.compile(r'.*03|=>.*')
          find_osm_sources = list(filter(regex.match, sources))
          if len(find_osm_sources) > 0:
             for id in find_osm_sources:
                  osm_objects += data[data.meta_ist == id].shape[0]
          fdata['osm_objects'] = osm_objects
          fdata['provice'] = province
          dfdata.append(fdata)
     pd.DataFrame(dfdata).to_parquet(province + "_dbsn.parquet",index=False)
     pd.DataFrame(dfdata).to_csv(province + "_dbsn.parquet",index=False)          

