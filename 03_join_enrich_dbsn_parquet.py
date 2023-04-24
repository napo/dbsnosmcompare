#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import glob
import os
pd.options.mode.chained_assignment = None
source_dir = "download"
start_dir = os.getcwd()
dest_dir = "data"
#03 join_enrich_dbsn_parquet.py

province_region = {'Matera': 'Basilicata',
                     'Potenza': 'Basilicata',
                     'Campobasso': 'Molise',
                     'Isernia': 'Molise',
                     'Pesaro e Urbino': 'Marche',
                     'Caserta': 'Campania',
                     'Catanzaro': 'Calabria',
                     'Ancona': 'Marche',
                     'Benevento': 'Campania',
                     'Reggio di Calabria': 'Calabria',
                     'Macerata': 'Marche',
                     'Napoli': 'Campania',
                     'Trapani': 'Sicilia',
                     'Ascoli Piceno': 'Marche',
                     'Avellino': 'Campania',
                     'Palermo': 'Sicilia',
                     'Massa Carrara': 'Toscana',
                     'Salerno': 'Campania',
                     'Messina': 'Sicilia',
                     'Lucca': 'Toscana',
                     "L'Aquila": 'Abruzzo',
                     'Agrigento': 'Sicilia',
                     'Pistoia': 'Toscana',
                     'Teramo': 'Abruzzo',
                     'Caltanissetta': 'Sicilia',
                     'Firenze': 'Toscana',
                     'Pescara': 'Abruzzo',
                     'Enna': 'Sicilia',
                     'Livorno': 'Toscana',
                     'Chieti': 'Abruzzo',
                     'Catania': 'Sicilia',
                     'Pisa': 'Toscana',
                     'Ragusa': 'Sicilia',
                     'Arezzo': 'Toscana',
                     'Foggia': 'Puglia',
                     'Siracusa': 'Sicilia',
                     'Siena': 'Toscana',
                     'Bari': 'Puglia',
                     'Grosseto': 'Toscana',
                     'Taranto': 'Puglia',
                     'Prato': 'Toscana',
                     'Viterbo': 'Lazio',
                     'Brindisi': 'Puglia',
                     'Cosenza': 'Calabria',
                     'Crotone': 'Calabria',
                     'Vibo Valentia': 'Calabria',
                     'Rieti': 'Lazio',
                     'Latina':'Lazio',
                     'Frosinone':'Lazio',
                     'Lecce': 'Puglia',
                     'Roma': 'Lazio',
                     'Fermo': 'Marche',
                     'Barletta-Andria-Trani': 'Puglia',
                     'Perugia':'Umbria',
                     'Terni':'Umbria',
                     'Cagliari':'Sardegna',
                     'Nuoro':'Sardegna',
                     'Oristano':'Sardegna',
                     'Sassari':'Sardegna',
                     'Sud Sardegna':'Sardegna'}


description_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRgAq3z8-cU_Fy88TUxteuTt_jsvUXIyFUFEbTrRuOXl2KFK-dbAgKAogJxUQtKkdPO5QzJm0M59Pw1/pub?gid=973898789&single=true&output=csv"
description_data = pd.read_csv(description_url)

description_data = description_data.applymap(lambda x: x.lower() if isinstance(x, str) else x)
description_data["macro_category_code"] = description_data["macro_category_code"].apply(lambda x: "{:02d}".format(x))
description_data["category_code"] = description_data["category_code"].apply(lambda x: "{:04d}".format(x))
description_data["code"] = description_data["code"].apply(lambda x: "{:06d}".format(x))

#os.getcwd()
os.chdir(source_dir)
dir_path = r'*_dbsn.parquet'
data_files = glob.glob(dir_path)
datafiles = []
for f in data_files:
    datafiles.append(pd.read_parquet(f))

data_igm_osm = pd.concat(datafiles)
data_igm_osm = data_igm_osm.fillna(0).reset_index()
del data_igm_osm['index']
columns = data_igm_osm.columns.unique()

data_igm_osm['region'] = data_igm_osm['provice'].apply(lambda x: province_region[x])
data_igm_osm.rename(columns={'provice':'province'},inplace=True)
data = pd.merge(data_igm_osm, description_data, left_on="name", right_on="layer_name")


data.to_parquet(start_dir + os.sep + dest_dir + os.sep + "data_igm_provenance_osm_provincies.parquet")

data.to_csv(start_dir + os.sep + dest_dir + os.sep  + "data_igm_provenance_osm_provincies.csv",index=False)

