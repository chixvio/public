targetScope = 'subscription'

@description('The name of the policy definition.')
param policyName string = 'DeployVmCpuAlert'

@description('Display name for the policy.')
param policyDisplayName string = 'Deploy VM CPU Alert'

@description('Alert threshold, in percent.')
param cpuThresholdPercent int

@description('Time window for the alert (ISO 8601).')
param windowSize string

@description('Evaluation frequency (ISO 8601).')
param evaluationFrequency string

@description('Action Group Resource ID for alert notifications.')
param actionGroupResourceId string

// Policy Definition - DeployIfNotExists
resource policyDef 'Microsoft.Authorization/policyDefinitions@2021-06-01' = {
  name: policyName
  properties: {
    displayName: policyDisplayName
    description: 'Ensures all Virtual Machines have a Percentage CPU metric alert deployed automatically.'
    mode: 'All'
    policyRule: {
      if: {
        field: 'type'
        equals: 'Microsoft.Compute/virtualMachines'
      }
      then: {
        effect: 'deployIfNotExists'
        details: {
          type: 'Microsoft.Insights/metricAlerts'
          roleDefinitionIds: [
            subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '749f88d5-cbae-40b8-bcfc-e573ddc772fa')
          ]
          deployment: {
            properties: {
              mode: 'incremental'
              template: json(loadTextContent('./ALERT-vmCpuPercentage.json'))
              parameters: {
                targetResourceId: { value: '[field(\'id\')]' }
                actionGroupId: { value: actionGroupResourceId }
                threshold: { value: cpuThresholdPercent }
                windowSize: { value: windowSize }
                frequency: { value: evaluationFrequency }
              }
            }
          }
          existenceCondition: {
            allOf: [
              {
                field: 'name'
                equals: 'vmCpuPercentageAlert'
              }
            ]
          }
        }
      }
    }
  }
}

output policyDefinitionId string = policyDef.id
