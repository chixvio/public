
$template_file  = "infrastructure\data_landing_zone\main.bicep"
$param_file     = "infrastructure\data_landing_zone\dlz_dev.bicepparam"
$location       = "uksouth"


az deployment sub create `
  --location $location `
  --template-file $template_file `
  --parameters $param_file `
  --debug
