import argparse

import signal
import sys

import requests

import json
from json import decoder
from bs4 import BeautifulSoup, SoupStrainer
import csv

# download latest API spec JSON file
urlImpinjPlatform = 'https://platform.impinj.com'
urlApiOverview = urlImpinjPlatform + '/site/docs/reader_api_welcome/index.gsp'
pageOverview = requests.get(urlApiOverview)
soup = BeautifulSoup(pageOverview.content, features="html.parser", parse_only=SoupStrainer('a'))
endpointDownloadJSON = soup.find_all('a', string='JSON format', limit=1)[0]['href']
urlDownloadJSON = urlImpinjPlatform + endpointDownloadJSON
print("Downloading API spec from: ", urlDownloadJSON)

fileApiJson = requests.get(urlDownloadJSON).content
stringApiJson = fileApiJson.decode("utf8")
jsonParsedFile = json.loads(stringApiJson)

paths = jsonParsedFile['paths']

endpoints = []

# build array of paths & REST commands
print('path list: ')
for path in paths:
    print(path)
    for key in paths[path].keys():
        print ("   ", key)
        endpoint = []
        endpoint.append(path)
        endpoint.append(key)
        endpoints.append(endpoint)
    
print(endpoints)

# setup CSV parameters
fields = ['Endpoint', 'Request Type']
rows = endpoints

filename = 'impinj_iot_dev_intfc_endpoints.csv'

# write to CSV file
with open(filename, 'w', newline='') as csvfile:
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)

