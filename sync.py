#!/usr/bin/env python
import requests, os, json, logging

# create logger
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# setup url for all incidents assigned to SNOW_USER
url = 'https://' + os.environ['SNOW_NAME'] + '.service-now.com/api/now/table/incident?active=true&assigned_to=' + os.environ['SNOW_USER']

# get all incidents
headers = {"Accept":"application/json"}
response = requests.get(url, auth=(os.environ['SNOW_USER'],os.environ['SNOW_PASS']), headers=headers, verify=True)

# log err and exit if not ok
if response.status_code != 200:
    logger.fatal("Unable to get incidents from SNow")
    exit(1)

# read-in each incident
results = json.loads(response.text)['result']
for incident in results:
    sys_id = incident['sys_id']
    title = incident['short_description']
    summary = incident['description']
    print(sys_id, title, summary)
