#!/usr/bin/env python
import requests, os, json, logging

# create logger
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# setup url for snow tenant (url) and user from env
url = 'https://' + os.environ['SNOW_URL'] + '.service-now.com/api/now/table/incident?active=true&assigned_to=' + os.environ['SNOW_USER']

# setup json header and make request using auth from env
headers = {"Accept":"application/json"}
response = requests.post(url, auth=(os.environ['SNOW_USER'],os.environ['SNOW_PASS']), headers=headers, verify=True)

# log err and exit if not 201
if response.status_code != 201:
    logger.fatal("Didn't receive 200 response code")
    exit(1)

logger.info(response.text)
