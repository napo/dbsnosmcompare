# dbsn osm compare

## Introduction
The **IGM** - **I**stituto **G**eografico **M**ilitare (Italian Military Geographical Institute) is the official national body that deals with cartography for Italy.
In September 2022 it released an important resource called **DBSN** - (**D**ata**B**ase di **S**intesi **N**azionale - National Synthesis Database) which - currently - covers 9 regions (Abruzzo, 'Basilicata, Calabria, Campania, Lazio, Marche, Molise, Puglia, Sicily, Tuscany).<br/>
The database is released under the ODbL license as part of the data derives from OpenStreetMap.<br/>
In this repository you can find a series of scripts that analyze how OpenStreetMap data is re-distributed by IGM.

### DBSN description
The DBSN resource is available at this address<br/>
[https://www.igmi.org/it/dbsn-database-di-sintesi-nazionale](https://www.igmi.org/it/dbsn-database-di-sintesi-nazionale)

Here an English translation of the introduction

---

The DBSN (National Synthesis Database) is a geographical database containing the most significant territorial information for carrying out thematic analyzes and representations at a national level. To create the DBSN, with the aim of processing increasingly complete and updated data, reference was mainly made to regional geo-topographic data as the primary source of information. In the initial phase of the project, data was collected in the most up-to-date version and a transformation of the structure was carried out to make it homogeneous at a national level, maintaining the original level of detail. Subsequently, it was integrated with data from national public bodies, for example the cadastral maps of the Revenue Agency, Istat data, data from other Ministries, also considering other information available on the web such as Open Street Map data (OSM). Where the derived information was not sufficient, data were acquired directly from orthoimages. In particular, in the re-elaboration of the contents, the viability is updated at least for the main connections; the administrative limits are derived from the cadastral ones and the municipal areas are made congruent with each other and with the state border; the building is classified according to the main categories of use. Furthermore, an updating and normalization activity was started for toponymy and is still in progress.<br/>
By constantly acquiring and integrating new data, the DBSN is continuously updated. From the content of the DBSN, in vector format, the cartography is derived at a scale of 1:25,000 through automatic procedures of cartographic generalization and application of the defined symbols.

---

Data specifications are available on this page.<br/>
[https://www.igmi.org/boaga_caloger_api4242_rosbind/dbsn/dbsn_specs_all.html](https://www.igmi.org/boaga_caloger_api4242_rosbind/dbsn/dbsn_specs_all.html
)

The authors of this repository created a [.csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vRgAq3z8-cU_Fy88TUxteuTt_jsvUXIyFUFEbTrRuOXl2KFK-dbAgKAogJxUQtKkdPO5QzJm0M59Pw1/pub?gid=973898789&single=true&output=csv) file which summarizes what is reported on the specifications page with some significant text in English

#### data download
Downloading to the DBSN is managed through registration.
However, since it is open data, the Italian OpenStreetMap community has created a copy of the data that can be accessed on this wiki page.
[https://wiki.openstreetmap.org/wiki/Italy/DBSN](https://wiki.openstreetmap.org/wiki/Italy/DBSN)

## Results
The directory [data](https://github.com/napo/dbsnosmcompare/tree/main/data) contains the results.
<br/>
Here a representation of the percentage of data from OpenStreetMap declared of the data of the Military Geographical Institute for the available Italian regions.<br/>
![](https://raw.githubusercontent.com/napo/dbsnosmcompare/main/image/output_italy.png)


## Scripts

Scripts to compare DBSN data from IGM with the OSM data
* [01_download_data.py](https://github.com/napo/dbsnosmcompare/blob/main/01_download_data.py)<br/>this script download all the data from DBSN and the geopackages openstreetmap data offered by Wikimedia Italia with the project [OSM Estratti](https://osmit-estratti.wmcloud.org/)<br/>
**NOTE**: this script download ~62Gb of files
* [02_osm_declaration_in_dbsn.py](https://github.com/napo/dbsnosmcompare/blob/main/02_osm_declaration_in_dbsn.py)<br/>this script creates csv and parquet files from all the DBSN data - separated by province - and calculate the number of objects for each layer and the number of objects tagged as "source from openstreetmap" by IGM.
* [03_join_enrich_dbsn_parquet.py](https://github.com/napo/dbsnosmcompare/blob/main/03_join_enrich_dbsn_parquet.py)<br/>this script collects all the files generated by the previous one and enriches the dataframe with the descriptions of the DBSN
* [04_analysis_osm_presence_igm_declaration.py](https://github.com/napo/dbsnosmcompare/blob/main/analysis_osm_presence_igm_declaration.ipynb)<br/>this script takes care of the creation of some statistics related to the OSM data declared by IGM.<br/>
The same script is also available as a [Jupyter Notebook]() to allow for further analysis.
* [05_check_osm_data_coverage.py](https://github.com/napo/dbsnosmcompare/blob/main/05_check_osm_data_coverage.py)
this script compares the km of streets mapped and the square km of building surface in OpenStreeMap with the data distributed by the italian Military Geographic Institute in order to identify how much work done by the mappers cover the official data.<br>For each Italian province, a .parquet file is generated which contains information on:<ul><li>kilometers of streets present in the IGM data</li><li>kilometers of streets present in the OSM data</li><li>kilometers of streets identified in the OSM which are present in the IGM</li><li>square kilometers of the surface of the buildings present in the IGM data</li><li>square kilometers of the surface of the buildings present in the OSM data</li><li>square kilometers of the surface of the buildings identified in the OSM which are mapped in the IGM</li></ul><b>NOTE</b>:<br/>IGM acquires data from OpenStreetMap if it doesn't find a match from the official sources it examines.
* show_data.ipynb
this script aggregate the data generated from investigate_data.ipnyb
