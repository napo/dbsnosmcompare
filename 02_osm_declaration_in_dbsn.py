#!/usr/bin/env python
# coding: utf-8

import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import fiona
import matplotlib.pyplot as plt
import pandas as pd
import re
source_dir = "download"
start_dir = os.getcwd()
#02_osm_declaration_in_dbsn.py


dir_list = os.listdir(source_dir)
provincies = [f.replace("_dbsn.gdb", "") for f in dir_list if "_dbsn.gdb" in f]
exclude = [
"Agrigento",
"Catanzaro",
"Benevento",
"Brindisi",
"Massa Carrara",
"Perugia",
"Ascoli Piceno",
"Napoli",
"Siena",
"Pesaro e Urbino",
"Pistoia",
"Pescara",
"Salerno",
"Livorno",
"Matera",
"Lecce",
"Ragusa",
"Bari",
"L'Aquila",
"Ancona",
"Enna",
"Arezzo",
"Teramo",
"Lucca",
"Frosinone",
"Grosseto",
"Fermo",
"Avellino",
"Rieti",
"Oristano",
"Sassari",
"Viterbo",
"Palermo",
"Nuoro",
"Foggia",
"Prato",
"Crotone",
"Trapani",
"Cagliari",
"Taranto",
"Cosenza",
"Caserta",
"Barletta-Andria-Trani",
"Pisa",
"Messina",
"Vibo Valentia",
"Chieti",
"Macerata",
"Reggio di Calabria",
"Caltanissetta",
"Catania",
"Firenze",
"Latina",
"Roma",
"Sud Sardegna",
"Isernia",
"Terni",
"Campobasso",
"Potenza",
"Siracusa"
]

# In[6]:


os.chdir(source_dir)


# In[8]:


for province in provincies:
     print(province)
     if province not in exclude:
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
          pd.DataFrame(dfdata).to_parquet(start_dir + os.sep + source_dir + os.sep + province + "_dbsn.parquet",index=False)
          pd.DataFrame(dfdata).to_csv(start_dir + os.sep + source_dir + os.sep + province + "_dbsn.csv",index=False)  
     print("next")
