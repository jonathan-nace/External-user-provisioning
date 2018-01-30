import json
import requests
import user_provision
from plugin import getApiToken, getUrl, inviteMessage, removalMessage

def inviteUser(email,configMap,allPermissions, plugin_tag):

    log = 'Slack: Instruction sent in email.\n'
    instruction = inviteMessage(configMap,plugin_tag)
    return user_provision.getJsonResponse(plugin_tag, email, log, instruction)

def removeUser(email,configMap,allPermissions, plugin_tag): #removes user as a member of dev-signiant
    #get team id
    team = requests.get("https://slack.com/api/team.info?token=" + getApiToken(configMap,plugin_tag) )
    my_json = team.content.decode('utf8')
    data = json.loads(my_json)
    teamId=data['team']['id']

    log = 'Slack: User removed from Slack dev-signiant.\n'
    instruction = email + removalMessage(configMap,plugin_tag)
    try:
        #get user id
        userId= requests.get(	"https://slack.com/api/auth.findUser?token=" + getApiToken(configMap,plugin_tag)+"&email="+email+"&team="+teamId )
        my_json = userId.content.decode('utf8')
        data = json.loads(my_json)
        slackUserID = data['user_id']

        #disable user
        user = requests.post("https://slack.com/api/users.admin.setInactive" + "?token=" + getApiToken(configMap,plugin_tag) + "&user="+slackUserID)
    except Exception as error:
        log = 'Slack: Remove from slack error:'+ email+' does not exist or is already inactive\n error: '+ str(error) +'\n'
        instruction = 'Remove from slack error:'+ email+'does not exist or is already inactive. Exception caught: '+ str(error)

    return user_provision.getJsonResponse(plugin_tag, email, log, instruction)
