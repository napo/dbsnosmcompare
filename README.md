# dbsn osm compare
Scripts to compare DBSN data from IGM with the OSM data
* investigate_data.ipynb
this script read all the sources of DBSN and compare the data for the streets and building with the relative OpenStreetMap data
* show_data.ipynb
this script aggregate the data generated from investigate_data.ipnyb
* from_osm_declarations.ipynb
this script extract the information about the declaration by IGM for each object collected in each dataset that comes from OpenStreetMap
* dbsn_from_osm.ipynb
this script aggregate the data extract from the script from_osm_declarations.ipynb
