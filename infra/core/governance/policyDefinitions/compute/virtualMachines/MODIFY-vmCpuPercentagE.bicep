targetScope = 'subscription'

@description('The name of the policy definition.')
param policyName string = 'ModifyVmCpuAlert'

@description('Display name for the policy.')
param policyDisplayName string = 'Modify VM CPU Alert Configuration'

@description('Alert threshold, in percent.')
param cpuThresholdPercent int

@description('Time window for the alert (ISO 8601).')
param windowSize string

@description('Evaluation frequency (ISO 8601).')
param evaluationFrequency string

@description('Action Group Resource ID for alert notifications.')
param actionGroupResourceId string

// Policy Definition - Modify existing alerts
resource policyDef 'Microsoft.Authorization/policyDefinitions@2021-06-01' = {
  name: policyName
  properties: {
    displayName: policyDisplayName
    description: 'Modifies existing VM CPU metric alerts to match the desired configuration.'
    mode: 'All'
    policyRule: {
      if: {
        allOf: [
          {
            field: 'type'
            equals: 'Microsoft.Insights/metricAlerts'
          }
          {
            field: 'name'
            equals: 'vmCpuPercentageAlert'
          }
          {
            field: 'Microsoft.Insights/metricAlerts/criteria.Microsoft-Azure-Monitor-SingleResourceMultipleMetricCriteria.allOf[*].metricNamespace'
            equals: 'Microsoft.Compute/virtualMachines'
          }
          {
            field: 'Microsoft.Insights/metricAlerts/criteria.Microsoft-Azure-Monitor-SingleResourceMultipleMetricCriteria.allOf[*].metricName'
            equals: 'Percentage CPU'
          }
        ]
      }
      then: {
        effect: 'modify'
        details: {
          roleDefinitionIds: [
            subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '749f88d5-cbae-40b8-bcfc-e573ddc772fa') // Monitoring Contributor
          ]
          operations: [
            {
              operation: 'addOrReplace'
              field: 'properties.criteria.allOf[0].threshold'
              value: cpuThresholdPercent
            }
            {
              operation: 'addOrReplace'
              field: 'properties.windowSize'
              value: windowSize
            }
            {
              operation: 'addOrReplace'
              field: 'properties.evaluationFrequency'
              value: evaluationFrequency
            }
            {
              operation: 'addOrReplace'
              field: 'properties.actions[0].actionGroupId'
              value: actionGroupResourceId
            } 
          ]
        }
      }
    }
  }
}

output policyDefinitionId string = policyDef.id
