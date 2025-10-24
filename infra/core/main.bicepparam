using 'main.bicep'


param location = 'uksouth' // Azure region for resources
param vmSize = 'Standard_B1s' // VM size enforced by policy
param emailAddress = 'chi.adiukwu@bdo.co.uk'
param teamsWebhookUrl = 'https://outlook.office.com/webhook/...' // Replace with your Teams webhook URL
param resourceGroupName = 'policy-test-rg'
