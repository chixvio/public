targetScope = 'subscription'

param adminEmail string
param tags object

// Create the Action Group for alert notifications
//-------------------------------------------------------------
module actionGroup './actionGroup.bicep' = {
  name: 'actionGroupDeploy'
  scope: resourceGroup('policy-test-rg')
  params: {
    actionGroupName: 'ag-policy-alerts'
    emailAddress: adminEmail
    tags: tags
  }
}

// VM CPU Alert Management Policy Set
//-------------------------------------------------------------

// 1. Deploy VM CPU Alert (DeployIfNotExists) Policy Definition
module vmCpuDeployPolicy 'policyDefinitions/compute/virtualMachines/DINE-vmCpuPercentage.bicep' = {
  name: 'vmCpuDeployPolicy'
  scope: subscription()
  params: {
    policyName: 'DeployVmCpuAlert'
    policyDisplayName: 'Deploy VM CPU Alert'
    cpuThresholdPercent: 5
    windowSize: 'PT15M'
    evaluationFrequency: 'PT5M'
    actionGroupResourceId: actionGroup.outputs.actionGroupId
  }
}

// 2. Deploy VM CPU Alert (Modify) Policy Definition
module vmCpuModifyPolicy 'policyDefinitions/compute/virtualMachines/MODIFY-vmCpuPercentage.bicep' = {
  name: 'vmCpuModifyPolicy'
  scope: subscription()
  params: {
    policyName: 'ModifyVmCpuAlert'
    policyDisplayName: 'Modify VM CPU Alert'
    cpuThresholdPercent: 5
    windowSize: 'PT15M'
    evaluationFrequency: 'PT5M'
    actionGroupResourceId: actionGroup.outputs.actionGroupId
  }
}

// 3. Create Policy Set (Initiative) combining both policies
module vmCpuPolicySet 'policySets/compute/virtualMachines/vmCpuManagement.bicep' = {
  name: 'vmCpuPolicySet'
  scope: subscription()
  params: {
    policySetName: 'VmCpuAlertManagement'
    policySetDisplayName: 'VM CPU Alert Management'
    deployPolicyDefinitionId: vmCpuDeployPolicy.outputs.policyDefinitionId
    modifyPolicyDefinitionId: vmCpuModifyPolicy.outputs.policyDefinitionId
    cpuThresholdPercent: 5
    windowSize: 'PT15M'
    evaluationFrequency: 'PT5M'
  }
}

// 4. Assign Policy Set with remediation
module vmCpuPolicySetAssignment 'policyAssignments/vmCpuManagement.bicep' = {
  name: 'vmCpuPolicySetAssignment'
  params: {
    policySetDefinitionId: vmCpuPolicySet.outputs.policySetDefinitionId
    assignmentDisplayName: 'VM CPU Alert Management'
    actionGroupResourceId: actionGroup.outputs.actionGroupId
    cpuThresholdPercent: 5
    windowSize: 'PT15M'
    evaluationFrequency: 'PT5M'
  }
}
