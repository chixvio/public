using 'main.bicep'

// Basic Settings
param name = 'policy-testing'
param location = 'uksouth'

// VM Settings
param adminSshKey = loadTextContent('../../../.ssh/debug_vm_key.pub')
param vmSize = 'Standard_B1s'
param createPublicIp = false

// SQL VM Settings
param createSqlVm = true
param sqlVmAdminUsername = 'sqluser'
@secure()
param sqlServerPassword = 'London_99!'  // Set this via deployment parameters
param networkAccessPolicy = 'AllowAll'
param appVmAdminPassword = 'London_99!'  // Set this via deployment parameters
param appVmAdminUsername = 'appuser'

// Network Settings
param vnetPrefix = '10.0.0.0/16'

// Resource Tags
param tags = {
	createdBy: 'dev'
	purpose: 'test-vm-low-cost'
}
