#!/usr/bin/env python
# coding: utf-8

# In[119]:


import pandas as pd
import os
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
from screeninfo import get_monitors
#04_analysis_osm_presence_igm_declaration.py


# In[120]:


data = pd.read_parquet("data" + os.sep + "data_igm_proveniance_osm_provincies.parquet")
data.rename(columns={'objects':'total_objects'},inplace=True)
# Raggruppiamo per regione e calcoliamo le percentuali
data_italy = data.groupby(['name_it', 'name_en','layer_name']).agg({'osm_objects': 'sum','total_objects': 'sum'}).reset_index()
data_region = data.groupby(['region','name_it', 'name_en','layer_name']).agg({'osm_objects': 'sum','total_objects': 'sum'}).reset_index()
data_provincies = data.groupby(['province','name_it', 'name_en','layer_name']).agg({'osm_objects': 'sum','total_objects': 'sum'}).reset_index()


# In[145]:


regions_label = ""
for r in data_region.region.unique():
    regions_label += r + " "


# In[143]:


regions_label


# In[121]:


data_italy['percentage'] = round(data_italy['osm_objects'] / data_italy['total_objects'] * 100,3)
data_italy_with_osm = data_italy[data_italy.percentage >= 1]
data_italy_with_osm['missing'] = 100 - data_italy_with_osm['percentage']
data_italy_with_osm = data_italy_with_osm.sort_values(by='percentage', ascending=False)


# In[148]:


monitor_width = int(get_monitors()[0].width)
fig, ax = plt.subplots(figsize=(monitor_width/100, 6))
plt.bar(data_italy_with_osm['name_en'], data_italy_with_osm['percentage'], color='b', label='Percentage')
#plt.bar(data_italy_with_osm['name_en'], data_italy_with_osm['missing'], bottom=data_italy_with_osm['percentage'], color='g', label='Missing')
plt.xlabel('Items')
plt.ylabel('Percentage')
ax.set_xticklabels(data_italy_with_osm['name_en'], rotation=45, ha='right')
plt.legend()
plt.suptitle("percentage of data from OpenStreetMap for each dataset managed by the Italian Military Geographical Institute")
plt.title("regions represented " + regions_label.rstrip())
plt.show()


# In[123]:


data_regione_with_osm_data = data_region[data_region.osm_objects > 0]
data_regione_with_osm_data['percentage'] = round(data_regione_with_osm_data['osm_objects'] / data_regione_with_osm_data['total_objects'] * 100,3)
data_regione_with_osm_data[data_regione_with_osm_data.percentage >= 1]


# In[124]:


data_provincies_with_osm_data = data_provincies[data_provincies.osm_objects > 0]
data_provincies_with_osm_data['percentage'] = round(data_provincies_with_osm_data['osm_objects'] / data_provincies_with_osm_data['total_objects'] * 100,3)
data_provincies_with_osm_data = data_provincies_with_osm_data[data_provincies.osm_objects > 0]


# In[125]:


#data_provincies_with_osm_data[data_provincies_with_osm_data['province'] == 'Ragusa'].sort_values(by="percentage", ascending=False)


# In[126]:


#data_regione_with_osm_data[data_regione_with_osm_data['region'] == 'Sicilia'].sort_values(by="percentage", ascending=False)


# In[127]:


#data_regione_with_osm_data.region.unique()


# In[128]:


data_italy


# In[ ]:





# In[129]:


data_italy[data_italy.percentage >= 1].sort_values(by="percentage", ascending=False)

