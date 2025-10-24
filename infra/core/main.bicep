targetScope = 'subscription'

@description('The Azure region for resource deployment')
param location string = 'uksouth'

@description('VM size to enforce in the VM configuration policy.')
param vmSize string = 'Standard_B1s'

@description('Email address for alert notifications')
param emailAddress string

@description('Teams Webhook URL for alert notifications')
param teamsWebhookUrl string

@description('Name of the resource group to create')
param resourceGroupName string 


// Deploy policies at subscription level
module subscriptionDeployment 'governance/policy/subscription_policies.bicep' = {
  name: 'subscriptionPolicies'
  params: {
    location: location
    vmSize: vmSize
    emailAddress: emailAddress
    teamsWebhookUrl: teamsWebhookUrl
    resourceGroupName: resourceGroupName
  }
}

output subscriptionPoliciesDeploymentName string = subscriptionDeployment.name
