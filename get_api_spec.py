import argparse

import signal
import sys

import requests

import json
from json import decoder
from bs4 import BeautifulSoup, SoupStrainer
import csv

urlImpinjPlatform = 'https://platform.impinj.com'

versions = [
    "1_0",
    "1_2",
    "1_3",
    "1_4",
    "1_5"
]

endpointsSpecUrl = []

for version in versions:
    endpoint = '/site/docs/reader_api_welcome/archive/v' + version + '/index.gsp'
    endpointsSpecUrl.append(endpoint)

# set current API version spec source (replace last version)
endpointsSpecUrl[len(endpointsSpecUrl)-1] = '/site/docs/reader_api_welcome/index.gsp' 

# get all API specs from impinj website
apiSpecs = []

for iteration, endpointSpecUrl in enumerate(endpointsSpecUrl):

    urlApiOverview = urlImpinjPlatform + endpointSpecUrl
    pageOverview = requests.get(urlApiOverview)
    soup = BeautifulSoup(pageOverview.content, features="html.parser", parse_only=SoupStrainer('a'))
    endpointDownloadJSON = soup.find_all('a', string='JSON format', limit=1)[0]['href']
    urlDownloadJSON = urlImpinjPlatform + endpointDownloadJSON
    print("Downloading API spec version " + versions[iteration] + " from: ", urlDownloadJSON)

    fileApiJson = requests.get(urlDownloadJSON).content
    stringApiJson = fileApiJson.decode("utf8")
    apiSpecs.append(json.loads(stringApiJson)['paths'])


# parse list of API endpoints from each full spec
for iteration, paths in enumerate(apiSpecs):

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

    filename = 'impinj_iot_dev_intfc_endpoints_v' + versions[iteration] + '.csv'

    # write to CSV file
    with open(filename, 'w', newline='') as csvfile:
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(rows)

