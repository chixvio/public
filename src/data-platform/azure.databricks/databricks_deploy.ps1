    param (
        [string]$DatabricksHost,
        [string]$DatabricksToken,
        [string]$Environment
    )

function Install-DatabricksCLI-Windows {

    $packageName = "Databricks.DatabricksCLI"

    # Helper function to check command existence
    function Command-Exists {
        param([string]$cmd)
        return (Get-Command $cmd -ErrorAction SilentlyContinue) -ne $null
    }

    # Early exit if Databricks CLI is already installed
    if (Command-Exists databricks) {
        Write-Host "Databricks CLI is already installed. Version:"
        databricks --version
        return
    }

    # Ensure winget is installed
    if (-not (Command-Exists winget)) {
        Write-Host "winget not found. Installing App Installer via Microsoft Store..."
        Start-Process "ms-windows-store://pdp/?productid=9NBLGGH4NNS1" -Wait
        Write-Error "Please install winget (App Installer) from Microsoft Store, then re-run this script."
        return
    } else {
        Write-Host "winget is already installed."
    }

    # Install Databricks CLI via winget
    Write-Host "Databricks CLI not found. Installing via winget..."
    winget install --id $packageName --accept-source-agreements --accept-package-agreements

    # Locate the executable in WinGet packages folder
    $wingetPackages = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages"
    if (-not (Test-Path $wingetPackages)) {
        Write-Error "WinGet Packages folder not found: $wingetPackages"
        return
    }

    Write-Host "Searching for databricks.exe in $wingetPackages ..."
    $databricksExe = Get-ChildItem -Path $wingetPackages -Recurse -Filter "databricks.exe" -ErrorAction SilentlyContinue | Select-Object -First 1

    if (-not $databricksExe) {
        Write-Error "Databricks CLI executable not found in WinGet packages folder."
        return
    }

    $databricksFolder = Split-Path $databricksExe.FullName
    Write-Host "Databricks CLI found at: $($databricksExe.FullName)"
    Write-Host "Adding folder to PATH: $databricksFolder"

    # Add folder to PATH if missing
    if (-not ($env:Path -split ";" | Where-Object { $_ -eq $databricksFolder })) {
        # Update current session
        $env:Path += ";" + $databricksFolder
        # Update user PATH permanently
        [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)
        Write-Host "Folder added to PATH successfully."
    } else {
        Write-Host "Folder is already in PATH."
    }

    # Verify Databricks CLI
    Write-Host "Verifying Databricks CLI installation..."
    if (Command-Exists databricks) {
        databricks --version
        Write-Host "Databricks CLI installed successfully and ready to use."
    } else {
        Write-Error "Databricks CLI could not be run. You may need to restart PowerShell for PATH changes to take effect."
    }
}



# Install CLI Linux  ----------------------------------------- #
function Install-DatabricksCLI-Linux {
    # Install Databricks CLI
    Write-Host "Installing Databricks CLI..."
    Invoke-Expression "curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh"
}



# ======================== FUNCTIONS ======================== #

# Configure and deploy Databricks bundle
function Deploy-DatabricksBundle {
    param (
        [Parameter(Mandatory=$true)]
        [string]$DatabricksHost,

        [Parameter(Mandatory=$true)]
        [string]$DatabricksToken,

        [Parameter(Mandatory=$true)]
        [string]$Environment
    )
    # Stop on errors
    $ErrorActionPreference = "Stop"

    # Helper to check if Databricks CLI exists
    function Command-Exists {
        param([string]$cmd)
        return (Get-Command $cmd -ErrorAction SilentlyContinue) -ne $null
    }

    if (-not (Command-Exists "databricks")) {
        Write-Error "Databricks CLI is not installed. Please install it before proceeding."
        return
    }

    Write-Host "Configuring Databricks CLI for host: $DatabricksHost"

    # Stop on errors
    $ErrorActionPreference = "Stop"

    # Configure Databricks CLI using token
    # Non-interactive authentication
    $env:DATABRICKS_HOST  = $DatabricksHost
    $env:DATABRICKS_TOKEN = $DatabricksToken

    # $databricksConfig = "`n$DatabricksToken"
    # $databricksConfig | databricks configure --token
    databricks bundle validate -t $Environment --var="databricks_host=$DatabricksHost"
    databricks bundle deploy -t $Environment --var="databricks_host=$DatabricksHost"


}


# ======================== MAIN EXECUTION ======================== #

Write-Host "`n======================== STARTING DEPLOYMENT ========================"


if ($env:OS -eq "Windows_NT") {
    Install-DatabricksCLI-Windows
} else {
    Install-DatabricksCLI-Linux
}

# Deploy bundle
cd src/azure.databricks
Deploy-DatabricksBundle -DatabricksHost $DatabricksHost -DatabricksToken $DatabricksToken -Environment $Environment
cd ../../



