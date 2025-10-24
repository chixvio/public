targetScope = 'subscription'

@description('The name of the policy set (initiative).')
param policySetName string = 'VmCpuAlertManagement'

@description('Display name for the policy set.')
param policySetDisplayName string = 'VM CPU Alert Management'

@description('ID of the deployIfNotExists policy definition.')
param deployPolicyDefinitionId string

@description('ID of the modify policy definition.')
param modifyPolicyDefinitionId string

@description('Alert threshold, in percent.')
param cpuThresholdPercent int = 80

@description('Time window for the alert (ISO 8601).')
param windowSize string = 'PT15M'

@description('Evaluation frequency (ISO 8601).')
param evaluationFrequency string = 'PT5M'

resource policySet 'Microsoft.Authorization/policySetDefinitions@2021-06-01' = {
  name: policySetName
  properties: {
    displayName: policySetDisplayName
    description: 'Manages VM CPU alerts by deploying new alerts and maintaining existing ones.'
    policyType: 'Custom'
    metadata: {
      category: 'Monitoring'
      version: '1.0.0'
    }
    parameters: {
      cpuThresholdPercent: {
        type: 'Integer'
        metadata: {
          displayName: 'CPU Threshold Percentage'
          description: 'The CPU percentage threshold that triggers the alert.'
        }
        defaultValue: cpuThresholdPercent
      }
      windowSize: {
        type: 'String'
        metadata: {
          displayName: 'Window Size'
          description: 'The time window for alert evaluation (ISO 8601).'
        }
        defaultValue: windowSize
      }
      evaluationFrequency: {
        type: 'String'
        metadata: {
          displayName: 'Evaluation Frequency'
          description: 'How often the alert is evaluated (ISO 8601).'
        }
        defaultValue: evaluationFrequency
      }
      actionGroupResourceId: {
        type: 'String'
        metadata: {
          displayName: 'Action Group Resource ID'
          description: 'The resource ID of the action group for alert notifications.'
        }
      }
    }
    policyDefinitions: [
      {
        policyDefinitionId: deployPolicyDefinitionId
        policyDefinitionReferenceId: 'Deploy_VM_CPU_Alert'
        parameters: {
          cpuThresholdPercent: {
            value: '[parameters(\'cpuThresholdPercent\')]'
          }
          windowSize: {
            value: '[parameters(\'windowSize\')]'
          }
          evaluationFrequency: {
            value: '[parameters(\'evaluationFrequency\')]'
          }
          actionGroupResourceId: {
            value: '[parameters(\'actionGroupResourceId\')]'
          }
        }
      }
      {
        policyDefinitionId: modifyPolicyDefinitionId
        policyDefinitionReferenceId: 'Modify_VM_CPU_Alert'
        parameters: {
          cpuThresholdPercent: {
            value: '[parameters(\'cpuThresholdPercent\')]'
          }
          windowSize: {
            value: '[parameters(\'windowSize\')]'
          }
          evaluationFrequency: {
            value: '[parameters(\'evaluationFrequency\')]'
          }
          actionGroupResourceId: {
            value: '[parameters(\'actionGroupResourceId\')]'
          }
        }
      }
    ]
  }
}

output policySetDefinitionId string = policySet.id
