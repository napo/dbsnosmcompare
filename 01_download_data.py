#!/usr/bin/env python
# coding: utf-8

# In[12]:


import requests
from bs4 import BeautifulSoup
import re
import os
import zipfile
import shutil


# In[5]:


# download DBSN data from wiki.openstreetmap.org
url = 'https://wiki.openstreetmap.org/wiki/Italy/DBSN'
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
tables = soup.findAll("table")
zip_links = {}
dest_dir = "download"
start_dir = os.getcwd()


# In[13]:


if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)


# In[14]:


for table in tables:
    for row in table.findAll('tr')[1:]:
        cells = row.findAll('td')
        for cell in cells:
            for link in cell.findAll('a'):
                if re.search('download$', link.get('href')):
                    name = cells[1].text
                    if str(name) != "-":
                        zip_links[name] = link.get('href')


# In[15]:


for province in zip_links.keys():
    file_url = zip_links[province]
    response = requests.get(file_url)
    zip_content = response.content
    with open('file.zip', 'wb') as f:
        f.write(zip_content)
    with zipfile.ZipFile('file.zip', 'r') as zip_ref:
        zip_ref.extractall(dest_dir)
    os.remove("file.zip")


# In[6]:


bad_dirs = []
directories = [name for name in os.listdir(dest_dir)
            if os.path.isdir(os.path.join(dest_dir, name))]

for directory in directories:
    if directory.find(".gdb") == -1:
        os.chdir(os.path.join(dest_dir, directory))
        subdirectories = [name for name in os.listdir('.')
                        if os.path.isdir(name)]
        for subdirectory in subdirectories:
            shutil.move(subdirectory, "..") 
        bad_dirs.append(directory)
    os.chdir(start_dir)
for bad_dir in bad_dirs:
    shutil.rmtree(start_dir+os.sep+dest_dir+os.sep+bad_dir)
      


# In[16]:


# download openstreetmap data from osmit-estratti


# In[73]:


url="https://osmit-estratti.wmcloud.org/boundaries/poly/limits_IT_provinces.json"
prefix_download = "https://osmit-estratti.wmcloud.org/"
response = requests.get(url)


# In[18]:


provincies = response.json()


# In[19]:


osm_sources = {}
for osm_province in provincies['objects']['limits_IT_provinces']['geometries']:
    try:
        province = osm_province['properties']['name']
        gpkg = osm_province['properties']['.gpkg']
        osm_sources[province] = gpkg
    except KeyError:
        pass


# In[67]:


dir_list = os.listdir(dest_dir)
gdb_dirs = [d for d in dir_list if d.endswith(".gdb")]


# In[68]:


new_dirs = []
for d in gdb_dirs:
    if d.endswith("_dbsn.gdb"):
        new_dirs.append(d[:-9])
    else:
        new_dirs.append(d)
new_dirs = [d.replace("Roma", "Roma Capitale") if d == "Roma" else d.replace("Massa Carrara", "Massa-Carrara") for d in new_dirs]
new_dirs = [d.replace("Oristano", "Aristanis/Oristano") for d in new_dirs]


# In[82]:


for gdbsource in new_dirs:
    try:
        downloadurl = prefix_download + osm_sources[gdbsource]
        response = requests.get(downloadurl)
        file_name = dest_dir + os.sep + osm_sources[gdbsource].replace("dati/poly/province/geopackage/","")[4:]
        with open(file_name, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(e)
        pass

