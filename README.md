# snow-jira-sync
Python utility scripts for synchronizing incidents on ServiceNow to JIRA. Used in lue of snow/jira extensions due to not having admin access to either.

## s2j
ServiceNow to JIRA sync. Pulls all incidents from SNow assigned to a specified user and creates issues (bugs) in JIRA. Closes incident once migrated.

#### Configuration
The following env vars should be setup for the s2j.py script:
* SNOW_NAME (snow tenant to logon, ie https://**tenant**.servicenow.com)
* SNOW_USER (snow user used to login as and to assign incidents to for sync with JIRA)
* SNOW_PASS (snow password used to login)

* JIRA_NAME (jira tenant to logon, ie https://**tenant**.atlassian.net)
* JIRA_PROJECT (jira project to create issues)
* JIRA_USER (jira user used to login)
* JIRA_TOKEN (jira api token used to login, see https://id.atlassian.com/manage/api-tokens)
