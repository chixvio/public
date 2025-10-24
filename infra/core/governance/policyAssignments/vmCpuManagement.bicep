targetScope = 'subscription'

@description('Policy set (initiative) definition ID to assign')
param policySetDefinitionId string

@description('Display name for the assignment')
param assignmentDisplayName string = 'VM CPU Alert Management Assignment'

@description('Action Group Resource ID for alert notifications')
param actionGroupResourceId string

@description('CPU threshold percentage')
param cpuThresholdPercent int = 80

@description('Window size for alert evaluation')
param windowSize string = 'PT15M'

@description('Evaluation frequency')
param evaluationFrequency string = 'PT5M'

@description('Role definition ID for the managed identity when deploying resources')
param deploymentRoleDefinitionId string = 'b24988ac-6180-42a0-ab88-20f7382dd24c'

// Create the assignment with system-assigned identity
resource policySetAssignment 'Microsoft.Authorization/policyAssignments@2021-06-01' = {
  name: '${replace(policySetDefinitionId, '/', '-')}-assign'
  location: deployment().location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: assignmentDisplayName
    policyDefinitionId: policySetDefinitionId
    enforcementMode: 'Default'
    parameters: {
      cpuThresholdPercent: {
        value: cpuThresholdPercent
      }
      windowSize: {
        value: windowSize
      }
      evaluationFrequency: {
        value: evaluationFrequency
      }
      actionGroupResourceId: {
        value: actionGroupResourceId
      }
    }
  }
}

// Assign Contributor role to the managed identity for deployments
resource miRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, 'DeployIfNotExists-Role', policySetAssignment.id)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', deploymentRoleDefinitionId)
    principalId: policySetAssignment.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Create remediation task
resource remediation 'Microsoft.PolicyInsights/remediations@2024-10-01' = {
  name: '${replace(policySetDefinitionId, '/', '-')}-remediation'
  properties: {
    policyAssignmentId: policySetAssignment.id
    resourceDiscoveryMode: 'ExistingNonCompliant'
  }
  dependsOn: [
    miRoleAssignment
  ]
}

output assignmentId string = policySetAssignment.id
