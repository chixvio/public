targetScope = 'subscription'

@description('Deployment environment (e.g., dev, test, prod)')
param environment string = 'dev'

@description('Prefix for resource naming convention')
param prefix string = '${environment}-dlz-uks'

@description('Name of the resource group')
param resource_group_name string = '${prefix}-rg'

@description('Name of the Databricks workspace')
param databricks_workspace_name string = '${prefix}-dbx'

@description('Location for the resources')
param location string = 'uksouth'

@description('SKU for Databricks workspace')
@allowed([
  'standard'
  'premium'
])
param sku string = 'premium'

var tags = {
  department:'IT'
}

resource resource_group 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resource_group_name
  location: location
  tags: tags
}


module databricks_workspace 'br/public:avm/res/databricks/workspace:0.11.4' = {
  name: '${prefix}-dbx'
  scope: resource_group
  params: {
    name: databricks_workspace_name
    tags: tags
    location: location
    skuName: sku
  }
}
