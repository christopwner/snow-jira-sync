#!/usr/bin/env python
import requests, os, json, logging

# create logger
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# setup url for all incidents assigned to SNOW_USER
snow_url = 'https://' + os.environ['SNOW_NAME'] + '.service-now.com/api/now/table/incident?active=true&assigned_to=' + os.environ['SNOW_USER']

# get all incidents
headers = {"Accept":"application/json"}
snow_response = requests.get(snow_url, auth=(os.environ['SNOW_USER'],os.environ['SNOW_PASS']), headers=headers, verify=True)

# log err and exit if unable to get snow incidents
if snow_response.status_code != 200:
    logger.fatal("Unable to get incidents from SNow")
    exit(1)

# setup jira query for all issues in project assigned to user and incomplete
jira_url = 'https://' + os.environ['JIRA_NAME'] + '.atlassian.net/rest/api/latest/search?jql=project=' \
        + os.environ['JIRA_PROJECT'] + '+and+assignee=' + os.environ['JIRA_ASSIGNEE'] + '+and+statusCategory!=done'

# get all issues
jira_response = requests.get(jira_url, auth=(os.environ['JIRA_USER'],os.environ['JIRA_TOKEN']), headers=headers, verify=True)

# log err and exit if unable to get jira tickets
if jira_response.status_code != 200:
    logger.fatal("Unable to get issues from JIRA")
    exit(1)

issues = json.loads(jira_response.text)['issues']

# read-in each incident
incidents = json.loads(snow_response.text)['result']
logger.debug('found %i incidents', len(incidents))
for incident in incidents:
    sys_id = incident['sys_id']
    summary = incident['short_description']
    description = incident['description']
    logger.debug('(%s, %s)', sys_id, summary);
