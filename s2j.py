#!/usr/bin/env python
import requests, os, json, logging

# create logger
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#headers = {"Accept":"application/json", "Content-Type":"application/json"}

# setup url for all incidents assigned to SNOW_USER
url = 'https://' + os.environ['SNOW_NAME'] + '.service-now.com/api/now/table/incident?assigned_to=' \
        + os.environ['SNOW_USER'] + '&active=true'

# get all incidents
response = requests.get(url, auth=(os.environ['SNOW_USER'],os.environ['SNOW_PASS']), verify=True)

# log err and exit if unable to get snow incidents
if response.status_code != 200:
    logger.fatal("Unable to get incidents from SNow")
    exit(1)
incidents = json.loads(response.text)['result']

# TODO set maxResults to disable pagination
# setup jira query for all issues in project assigned to user and incomplete
url = 'https://' + os.environ['JIRA_NAME'] + '.atlassian.net/rest/api/latest/search?jql=project=' \
        + os.environ['JIRA_PROJECT'] + '+and+labels=snow+and+statusCategory!=done'

# get all issues
response = requests.get(url, auth=(os.environ['JIRA_USER'],os.environ['JIRA_TOKEN']), verify=True)

# log err and exit if unable to get jira tickets
if response.status_code != 200:
    logger.fatal("Unable to get issues from JIRA")
    exit(1)
issues = json.loads(response.text)['issues']

# jira customfield to store snow id
customfield = os.environ['JIRA_FIELD']

# create issue dictionary based on snow ids
snowissues = {}
logger.debug('found %i issue(s)', len(issues))
for issue in issues:
    snowissues['021fa4070f8533c01cfedb0be1050e37'] = issue
    #snowissues[issue['fields'][customfield]] = issue

# read-in each incident
logger.debug('found %i incident(s)', len(incidents))
for incident in incidents:
    if incident['sys_id'] in snowissues:
        logger.debug('updating (%s, %s)', incident['sys_id'], incident['short_description']) 
    else:
        # setup data for new issue
        logger.debug('creating (%s, %s)', incident['sys_id'], incident['short_description'])
        data = { 'fields' : {'project' : {'key' : 'ROYAL'}, 'summary' : incident['short_description'], 'labels' : ['SNow'], \
                'description': incident['description'], 'issuetype' : {'name' : 'Bug'}, customfield : incident['sys_id'] }}
        json = json.dumps(data)
        logger.debug(json)
        
        # setup url to create issue and post
        url = 'https://' + os.environ['JIRA_NAME'] + '.atlassian.net/rest/api/latest/issue/'
        response = requests.post(url, auth=(os.environ['JIRA_USER'],os.environ['JIRA_TOKEN']), headers={"Content-Type":"application/json"}, json=data, verify=True)
        
        # log err and exit if unable to create jira issue
        if response.status_code != 200:
            logger.fatal("Unable to create issue(s) on JIRA")
            exit(1)

    #sys_id = incident['sys_id']
    #summary = incident['short_description']
    #description = incident['description']
