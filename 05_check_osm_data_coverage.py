#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import fiona
import pandas as pd
gpkg_suffix = "_poly.gpkg"
gdb_suffix = "_dbsn.gdb"
#05_check_osm_data_coverage.py
from shapely.strtree import STRtree


source_dir = "download"
start_dir = os.getcwd()


# In[3]:


dir_list = os.listdir(source_dir)
provincies = [f.replace("_poly.gpkg", "") for f in dir_list if "_poly.gpkg" in f]
# In[4]:


province_regioni = {'Matera': 'Basilicata',
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
                     'Crotone': 'Calabria',
                     'Vibo Valentia': 'Calabria',
                     'Cosenza': 'Calabria',
                     'Rieti': 'Lazio',
                     'Latina': 'Lazio',
                     'Lecce': 'Puglia',
                     'Roma': 'Lazio',
                     'Frosinone':'Lazio',
                     'Fermo': 'Marche',
                     'Barletta-Andria-Trani': 'Puglia',
                     'Perugia':'Umbria',
                     'Terni':'Umbria',
                     'Cagliari':'Sardegna',
                     'Nuoro':'Sardegna',
                     'Oristano':'Sardegna',
                     'Sassari':'Sardegna',
                     'Sud Sardegna':'Sardegna'}


# In[5]:


def getdata(osm_source,igm_source,prefix=source_dir + os.sep):
    data = {}
    #building_source = {}
    street_source = {}
    osm_source = prefix + osm_source
    igm_source = prefix + igm_source
    igm_layers_list = fiona.listlayers(igm_source)
    lines_osm = gpd.read_file(osm_source,layer="lines",driver="GPKG")
    multipolygons_osm = gpd.read_file(osm_source,layer="multipolygons",driver="GPKG")
    buildings_osm = multipolygons_osm.dropna(subset=['building'])
    all_buildings_osm = pd.concat([buildings_osm.geometry, 
                                   multipolygons_osm.dropna(subset=['shop']).geometry, 
                                    multipolygons_osm.dropna(subset=['amenity']).geometry, 
                                    multipolygons_osm.dropna(subset=['craft']).geometry,
                                    multipolygons_osm.dropna(subset=['military']).geometry,
                                    multipolygons_osm.dropna(subset=['office']).geometry,
                                    multipolygons_osm.dropna(subset=['tourism']).geometry],
                                  ignore_index=True)
    buildings_igm = gpd.read_file(igm_source,driver="FileGDB",layer="edifc")
    buildings_igm_small = gpd.read_file(igm_source,driver="FileGDB",layer="edi_min")
    #all_buildings_igm = pd.concat([buildings_igm_small.geometry, buildings_igm.geometry], ignore_index=True)
    #all_buildings_igm = gpd.GeoDataFrame(geometry=gpd.GeoSeries(all_buildings_igm))
    buildings_osm = all_buildings_osm.to_crs(buildings_igm.crs)
    
    # add_igm_streets = False
    # add_igm_footway = False
    # add_igm_mix = False
    # streets_igm_sources = []
    # length_streets_from_osm = 0
    # if "tr_str" in igm_layers_list:
    #     igm_streets = gpd.read_file(igm_source,layer="tr_str")
    #     igm_strees_in_osm = igm_streets
    #     if igm_strees_in_osm.shape[0] > 0:
    #         length_streets_from_osm = igm_strees_in_osm.length.sum()
    #     add_igm_streets= True
    #     streets_igm_sources.append(pd.DataFrame(igm_streets.meta_ist.value_counts()).reset_index().rename(columns={"index":"meta_ist","meta_ist":"totale"}))
    # if "ar_vms" in igm_layers_list:    
    #     igm_footway = gpd.read_file(igm_source,layer="ar_vms")
    #     #igm_footway = igm_footway.replace(to_replace='.*=>.*', value='03', regex=True)
    #     #igm_strees_in_osm = igm_footway[igm_footway.meta_ist == "03"]
    #     if igm_strees_in_osm.shape[0] > 0:
    #         length_streets_from_osm += igm_strees_in_osm.length.sum()
    #     add_igm_footway = True
    #     streets_igm_sources.append(pd.DataFrame(igm_footway.meta_ist.value_counts()).reset_index().rename(columns={"index":"meta_ist","meta_ist":"totale"}))
    # if "el_vms" in igm_layers_list:
    #     igm_mix = gpd.read_file(igm_source,layer="el_vms")
    #     #igm_mix = igm_mix.replace(to_replace='.*=>.*', value='03', regex=True)
    #     #igm_strees_in_osm = igm_mix[igm_mix.meta_ist == "03"]
    #     if igm_strees_in_osm.shape[0] > 0:
    #         length_streets_from_osm += igm_strees_in_osm.length.sum()
    #     add_igm_mix = True
    # streets_igm_sources.append(pd.DataFrame(igm_mix.meta_ist.value_counts()).reset_index().rename(columns={"index":"meta_ist","meta_ist":"totale"}))
    # lines_osm = lines_osm.to_crs(igm_streets.crs)
    # if add_igm_streets:
    #     all_streets_igm = igm_streets
    # if add_igm_footway:
    #     all_streets_igm = pd.concat([all_streets_igm.geometry, igm_footway.geometry], ignore_index=True)
    # if add_igm_mix:
    #     all_streets_igm = pd.concat([all_streets_igm.geometry, igm_mix.geometry], ignore_index=True)
    # count_streets_igm_sources = pd.DataFrame()
    # for strestreets_igm_source in streets_igm_sources:
    #     count_streets_igm_sources = pd.concat([count_streets_igm_sources, strestreets_igm_source])
    # count_streets_igm_sources = count_streets_igm_sources.groupby('meta_ist').sum().reset_index()
    # for idx in count_streets_igm_sources.meta_ist.unique():
    #     #if idx.find("=>") > -1:
    #     #    street_source["streets_source_03"] = count_streets_igm_sources[count_streets_igm_sources.meta_ist == idx].totale.values[0]
    #     #else:
    #     street_source["streets_source_" + idx] = count_streets_igm_sources[count_streets_igm_sources.meta_ist == idx].totale.values[0]
    # all_streets_igm= gpd.GeoDataFrame(geometry=gpd.GeoSeries(all_streets_igm))  
    # osm_streets = lines_osm[lines_osm.highway.isin(['unclassified','trunk_link','trunk','tertiary_link','tertiary', 'service', 'secondary_link','secondary','road','residential','primary_link','primary','pedestrian','living_street','construction'])]
    # osm_footways = lines_osm[lines_osm.highway.isin(['footway','cycleway','track','path','pedestrian','steps'])]
    # all_streets_osm = pd.concat([osm_footways.geometry, osm_streets.geometry], ignore_index=True)
    # all_streets_osm= gpd.GeoDataFrame(geometry=gpd.GeoSeries(all_streets_osm))    
    # province_border = gpd.read_file(igm_source,driver="FileGDB",layer="provin")
    # all_streets_osm = gpd.clip(all_streets_osm, province_border, keep_geom_type=True)
    data['osm_buildings'] = buildings_osm
    data['igm_buildings'] = buildings_igm
    data['igm_buildings_small'] = buildings_igm_small
    #data['igm_streets'] = all_streets_igm
    #data['osm_streets'] = all_streets_osm
    #data['igm_streets_sources'] = street_source 
    return(data)


def coverageBuildings(buildings_osm,buildings_igm,buildings_igm_small):
    data = {}
    points_buildings_osm = buildings_osm.geometry.representative_point()
    points_buildings_osm = gpd.GeoDataFrame(geometry=gpd.GeoSeries(points_buildings_osm))
    #osm_buildings_in_igm = gpd.sjoin(buildings_igm, points_buildings_osm, predicate='contains')
    #area_osm_buildings_in_igm  = buildings_osm[buildings_osm.index.isin(osm_buildings_in_igm.index.unique())].geometry.area.sum()
    
    points_osm = list(buildings_osm.geometry.representative_point().values)
    strtree = STRtree(points_osm) 
    crossbuildingidxs = []
    for idx,row in buildings_igm.iterrows():
        cross = strtree.query(row.geometry)
        if len(cross) > 0:
            crossbuildingidxs.append(idx)
    crossbuildingidxs = list(set(crossbuildingidxs))
    area_osm_buildings_in_igm  = buildings_igm[buildings_igm.index.isin(crossbuildingidxs)].geometry.area.sum()

    #points_osm = list(buildings_osm.geometry.representative_point().values)
    #strtree = STRtree(points_osm) 
    crossbuildingidxs = []
    for idx,row in buildings_igm_small.iterrows():
        cross = strtree.query(row.geometry)
        if len(cross) > 0:
            crossbuildingidxs.append(idx)
    crossbuildingidxs = list(set(crossbuildingidxs))
    area_osm_buildings_in_igm += buildings_igm_small[buildings_igm_small.index.isin(crossbuildingidxs)].geometry.area.sum()


    # points_igm = buildings_igm.geometry.representative_point()
    # points_buildings_igm = gpd.GeoDataFrame(geometry=gpd.GeoSeries(points_igm))
    # igm_buildings_in_osm = gpd.sjoin(buildings_osm, points_buildings_igm, predicate='contains')
    # area_igm_buildings_in_osm  = buildings_igm[buildings_igm.index.isin(igm_buildings_in_osm.index.unique())].geometry.area.sum()
    
    data['area_osm_buildings'] = [buildings_osm.geometry.area.sum()] 
    data['area_igm_buildings'] = [buildings_igm.geometry.area.sum()]   
    data['area_osm_in_igm_buildings'] = [area_osm_buildings_in_igm]
    # data['area_igm_buildings_in_osm'] = [area_igm_buildings_in_osm]
    return(data)


# In[7]:


def coverageStreets(streets_osm,streets_igm):
    data = {}
    common_streets = gpd.sjoin(streets_osm, streets_igm, predicate='intersects')    
    length = streets_osm[streets_osm.index.isin(common_streets.index.unique())].geometry.length.sum()
    data['osm_in_igm_streets_length'] = [length]
    data['osm_streets_length'] = [streets_osm.geometry.length.sum()]
    data['igm_streets_length'] = [streets_igm.geometry.length.sum()]
    return(data)


# In[8]:


data_analysis = pd.DataFrame()
nolist = [] #if you need to exclude some places simply
#if you add names to the list following the correct syntax they will be excluded from the analysis
nolist.append("Nuoro")
nolist.append("Lecce")
#nolist.append("Rieti")
nolist.append("Firenze")
nolist.append("Teramo")
nolist.append("Grosseto")
nolist.append("Pescara")
nolist.append("Sassari")
nolist.append("Macerata")
nolist.append("Messina")
nolist.append("Terni")
nolist.append("Caltanissetta")
nolist.append("Benevento")
nolist.append("Avellino")
nolist.append("Catanzaro")
nolist.append("Vibo Valentia")
nolist.append("Caserta")
nolist.append("Ancona")
nolist.append("Ascoli Piceno")
nolist.append("Arezzo")
nolist.append("Napoli")
nolist.append("Potenza")
nolist.append("Salerno")
nolist.append("Palermo")
nolist.append("Barletta-Andria-Trani")
nolist.append("Pisa")
nolist.append("Bari")
nolist.append("Matera")
nolist.append("Viterbo")
nolist.append("Reggio di Calabria")
nolist.append("Lucca")
nolist.append("Trapani")
nolist.append("Ragusa")
nolist.append("Enna")
nolist.append("Prato")
nolist.append("Isernia")
nolist.append("Crotone")
nolist.append("Livorno")
nolist.append("Fermo")
nolist.append("Cosenza")
nolist.append("Roma")
nolist.append("Latina")
nolist.append("Siracusa")
nolist.append("Massa Carrara")
nolist.append("Catania")
nolist.append("Frosinone")
nolist.append("Chieti")
nolist.append("Perugia")
nolist.append("Foggia")
nolist.append("Campobasso")
nolist.append("Cagliari")
nolist.append("Taranto")
nolist.append("L'Aquila")
nolist.append("Pesaro e Urbino")
nolist.append("Agrigento")
nolist.append("Sud Sardegna")
nolist.append("Oristano")
nolist.append("Pistoia")
nolist.append("Siena")
nolist.append("Brindisi")


for province in provincies:
    if province not in nolist:
        print(province)
        data_province = getdata(province+gpkg_suffix,province+gdb_suffix)
        data_buildings = coverageBuildings(data_province['osm_buildings'],data_province['igm_buildings'],data_province['igm_buildings_small'])
        #data_streets = coverageStreets(data_province['osm_streets'],data_province['igm_streets'])
        #data_buildings.update(data_streets)
        data_buildings['province'] = [province]
        data_buildings['region'] = [province_regioni[province]]
        data_analysis = pd.DataFrame(data=data_buildings)
        data_analysis.to_parquet(source_dir + os.sep + province+".parquet")


# In[9]:


print("Done")

