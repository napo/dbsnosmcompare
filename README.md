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


## Scripts

Scripts to compare DBSN data from IGM with the OSM data
* [01_download_data.py](https://github.com/napo/dbsnosmcompare/blob/main/01_download_data.py)<br/>this script download all the data from DBSN and the geopackages openstreetmap data offered by Wikimedia Italia with the project [OSM Estratti](https://osmit-estratti.wmcloud.org/)<br/>
**NOTE**: this script download ~62Gb of files
* investigate_data.ipynb
this script read all the sources of DBSN and compare the data for the streets and building with the relative OpenStreetMap data
* show_data.ipynb
this script aggregate the data generated from investigate_data.ipnyb
* from_osm_declarations.ipynb
this script extract the information about the declaration by IGM for each object collected in each dataset that comes from OpenStreetMap
* dbsn_from_osm.ipynb
this script aggregate the data extract from the script from_osm_declaraions.ipynb
