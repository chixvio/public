

$zone = "web-app"

$template_file  = "infra\${zone}\main.bicep"
$param_file     = "infra\${zone}\main.bicepparam"
$location       = "uksouth"


az deployment sub create `
  --location $location `
  --template-file $template_file `
  --parameters $param_file `
  --debug




#  az group delete --name 'app-test-rgdev-dlz-uks-rg' --yes


# Add Phrase to generate SSH Key
# ssh-keygen -t rsa -b 2048 -f $env:USERPROFILE\.ssh\debug_vm_key -N ""

# az policy state trigger-scan --subscription '06b7e703-eadf-4873-9d45-5a91459a0112'

# az policy remediation list --subscription '06b7e703-eadf-4873-9d45-5a91459a0112'