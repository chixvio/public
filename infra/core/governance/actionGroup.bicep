targetScope = 'resourceGroup'

param actionGroupName string
param tags object
param emailAddress string

var shortName = replace(actionGroupName, '-', '')

resource actionGroup 'Microsoft.Insights/actionGroups@2021-09-01' = {
  name: actionGroupName
  location: 'Global'  
  tags: tags
  properties: { 
    groupShortName: length(shortName) <= 12 ? shortName : substring(shortName, 0, 12)
    enabled: true
    emailReceivers: [
      {
        name: 'emailReceiver1'
        emailAddress: emailAddress
      }
    ]
  } 
}


output actionGroupId string = actionGroup.id
