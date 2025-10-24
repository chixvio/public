targetScope = 'subscription'

@description('SQL Server SA password when creating SQL VM')
@secure()
param sqlServerPassword string

param sqlVmAdminUsername string

@secure()
param appVmAdminPassword string

param appVmAdminUsername string

@description('Debug Bicep file to deploy a low-cost Linux VM for testing purposes')
param name string = 'policy-test'

@description('Location for all resources')
param location string

@description('SSH public key for the admin user (openssh)')
param adminSshKey string

@description('Size of the VM (kept small to reduce cost). Default: Standard_B1s')
param vmSize string = 'Standard_B1s'

@description('Create a public IP for testing (false by default to reduce costs)')
param createPublicIp bool = true

@description('Create a dedicated VM for SQL Server')
param createSqlVm bool = false

@description('Tags to apply to resources')
param tags object = {
	createdBy: 'dev'
	purpose: 'test-vm-low-cost'
}

@description('Network access policy for the VMs')
param networkAccessPolicy string = 'DenyAll'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${name}-rg'
  location: location
}


// (removed inline virtual network - using AVM module below)
// Virtual network (use AVM module)
@description('CIDR prefix for the vnet address space. Change when integrating with other networks.')
param vnetPrefix string = '10.0.0.0/16'

module virtualNetwork 'br/public:avm/res/network/virtual-network:0.7.1' = {
	name: 'virtualNetworkDeployment'
	scope: resourceGroup
	params: {
		// required
		addressPrefixes: [ vnetPrefix ]
		name: '${name}-vnet'

		// non-required but useful to pass
		location: location
		subnets: [
			{
				name: 'default'
				addressPrefix: '10.0.0.0/24'
			}
		]
		tags: tags
	}
}


module publicIp 'br/public:avm/res/network/public-ip-address:0.9.1' = if (createPublicIp) {
  name: 'publicIpAddressDeployment'
  scope: resourceGroup
  params: {
    name: '${name}-pip'
    location: location
    skuName: 'Basic'
    publicIPAllocationMethod: 'Dynamic'
    tags: tags
  }
}


module nsg 'br/public:avm/res/network/network-security-group:0.5.2' = {
  name: 'networkSecurityGroupDeployment'
  scope: resourceGroup
  params: {
    name: '${name}-nsg'
    location: location
    tags: tags
    securityRules: [
      {
        name: 'Allow-SSH'
        properties: {
          priority: 1000
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourcePortRange: '*'
          destinationPortRange: '22'
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
        }
      }
    ]
  }
}



module vm 'br/public:avm/res/compute/virtual-machine:0.20.0' = {
  name: 'linuxVirtualMachineDeployment'
  scope: resourceGroup
  params: {
    name: '${name}-linux-vm'
    location: location
    tags: tags
    vmSize: vmSize

    bootDiagnostics: true
    networkAccessPolicy: networkAccessPolicy
    adminUsername: appVmAdminUsername
    adminPassword: appVmAdminPassword
    availabilityZone: 1
    osType: 'Linux'
    imageReference: {
      publisher: 'Canonical'
      offer: '0001-com-ubuntu-server-jammy'
      sku: '22_04-lts'
      version: 'latest'
    }
    nicConfigurations: [
      {
        enableAcceleratedNetworking: false
        ipConfigurations: [
          {
            name: 'ipconfig1'
            subnetResourceId: virtualNetwork.outputs.subnetResourceIds[0]
            privateIPAllocationMethod: 'Dynamic'
            pipConfiguration: createPublicIp ? {
              allocationMethod: 'Dynamic'
            } : null
          }
        ]
        
      }
    ]
    osDisk: {
      diskSizeGB: 30
      managedDisk: {
        storageAccountType: 'Standard_LRS'
      }
    }
  }
}


module sqlVm 'br/public:avm/res/compute/virtual-machine:0.20.0' = if (createSqlVm) {
  scope: resourceGroup
  params: {
    name: '${name}-sql-vm'
    location: location
    tags: tags
    vmSize: vmSize
    availabilityZone: 1
    osType: 'Linux'
    imageReference: {
      publisher: 'Canonical'
      offer: '0001-com-ubuntu-server-jammy'
      sku: '22_04-lts'
      version: 'latest'
    }
    extensionCustomScriptConfig: {
      name: 'setupSqlServer'
      typeHandlerVersion: '2.1'
      settings: {
        fileUris: [
          'https://raw.githubusercontent.com/YOUR_REPO/setup-sqlserver.sh'
        ]
      }
      protectedSettings: {
        commandToExecute: 'MSSQL_SA_PASSWORD="${sqlServerPassword}" bash setup-sqlserver.sh'
      }
    }
    disablePasswordAuthentication: true
    publicKeys: [
      {
        path: '/home/${sqlVmAdminUsername}/.ssh/authorized_keys'  // <-- make sure this matches admin username param
        keyData: adminSshKey
      }
    ]
    bootDiagnostics: true
    networkAccessPolicy: networkAccessPolicy
    adminUsername: sqlVmAdminUsername
    nicConfigurations: [
      {
        enableAcceleratedNetworking: false
        ipConfigurations: [
          {
            name: 'ipconfig1'
            subnetResourceId: virtualNetwork.outputs.subnetResourceIds[0]
            privateIPAllocationMethod: 'Dynamic'
            pipConfiguration: createPublicIp ? {
              allocationMethod: 'Dynamic'
            } : null
          }
        ]
      }
    ]
    osDisk: {
      diskSizeGB: 30
      managedDisk: {
        storageAccountType: 'Standard_LRS'
      }
    }
  }
}

