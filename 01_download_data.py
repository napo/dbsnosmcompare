#!/usr/bin/env python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import os
import zipfile
import shutil
url = 'https://wiki.openstreetmap.org/wiki/Italy/DBSN'
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
tables = soup.findAll("table")
zip_links = {}
dest_dir = "download"
start_dir = os.getcwd()

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)


for table in tables:
    for row in table.findAll('tr')[1:]:
        cells = row.findAll('td')
        for cell in cells:
            for link in cell.findAll('a'):
                if re.search('download$', link.get('href')):
                    name = cells[1].text
                    if str(name) != "-":
                        zip_links[name] = link.get('href')


for province in zip_links.keys():
    file_url = zip_links[province]
    response = requests.get(file_url)
    zip_content = response.content
    with open('file.zip', 'wb') as f:
        f.write(zip_content)
    with zipfile.ZipFile('file.zip', 'r') as zip_ref:
        zip_ref.extractall(dest_dir)
    os.remove("file.zip")


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
      

