#
# This script scan each VM in scope to detect if SQL server insstalled and if it is regsitered with IaaS extension.
# The report includes the following information for each VM.
#
# Subscription Name
# Subscription ID
# ResourceGroupName
# Server Name
# Location
# Server SKU
# Size in vCores
# OS Type
# OS Version
# SQL Version
# SQL Edition
# IaaS registration status
#
# The script accepts the following command line parameters:
#
# -SubId [subscription_id]        (Optional. If not specified all subscription the user has access to Accepts a .csv file with the list of subscriptions)
# -FilePath [csv_file_name]       (Optional. Sprcifies a .csv file to save the data. if not specified, saves it in sql-vcm-inventory.csv)
#

param (
    [Parameter (Mandatory= $false)]
    [string] $SubId,
    [Parameter (Mandatory= $false)]
    [string] $FilePath

)

function CheckModule ($m) {

    # This function ensures that the specified module is imported into the session
    # If module is already imported - do nothing

    if (!(Get-Module | Where-Object {$_.Name -eq $m})) {
         # If module is not imported, but available on disk then import
        if (Get-Module -ListAvailable | Where-Object {$_.Name -eq $m}) {
            Import-Module $m
        }
        else {

            # If module is not imported, not available on disk, but is in online gallery then install and import
            if (Find-Module -Name $m | Where-Object {$_.Name -eq $m}) {
                Install-Module -Name $m -Force -Verbose -Scope CurrentUser
                Import-Module $m
            }
            else {

                # If module is not imported, not available and not in online gallery then abort
                write-host "Module $m not imported, not available and not in online gallery, exiting."
                EXIT 1
            }
        }
    }
}

function GetVCores {
    # This function translates each VM or Host sku type and name into vCores

     [CmdletBinding()]
     param (
         [Parameter(Mandatory)]
         [string]$type,
         [Parameter(Mandatory)]
         [string]$name
     )

     if ($global:VM_SKUs.Count -eq 0){
         $global:VM_SKUs = Get-AzComputeResourceSku  "westus" | where-object {$_.ResourceType -in 'virtualMachines','hostGroups/hosts'}
     }
     # Select first size and get the VCPus available
     $size_info = $global:VM_SKUs | Where-Object {$_.ResourceType.Contains($type) -and ($_.Name -eq $name)} | Select-Object -First 1

     # Save the VCPU count
     switch ($type) {
         "hosts" {$vcpu = $size_info.Capabilities | Where-Object {$_.name -eq "Cores"} }
         "virtualMachines" {$vcpu = $size_info.Capabilities | Where-Object {$_.name -eq "vCPUsAvailable"} }
     }

     if ($vcpu){
         return $vcpu.Value
     }
     else {
         return 0
     }
 }

function DiscoveryOnWindows {

# This script checks if SQL Server is installed on Windows

    [string] $SqlInstalled = ""
    $regPath = 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server'
    if (Test-Path $regPath) {
        $inst = (get-itemproperty $regPath).InstalledInstances
        #$SqlInstalled = ($inst.Count -gt 0)
        foreach ($i in $inst) {
            # Read registry data
            #
            $p = (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\Instance Names\SQL').$i
            $setupValues = (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\$p\Setup")
            $edition = ($setupValues.Edition -split ' ')[0]
            $version = ($setupValues.Version)
            $SqlInstalled =  $version, $edition -join ':'
        }
    }
    Write-Output $SqlInstalled
}

#
# This script checks if SQL Server is installed on Linux
#
#
$DiscoveryOnLinux =
    'if ! systemctl is-active --quiet mssql-server.service; then dir

    echo "False"
    exit
    else
        echo "True"
    fi'



# Ensure that the required modules are imported
# In Runbooks these modules must be added to the automation account manually

$requiredModules = @(
    "Az.Accounts",
    "Az.Compute",
    "Az.DataFactory",
    "Az.Resources",
    "Az.Sql",
    "Az.SqlVirtualMachine"
)
$requiredModules | Foreach-Object {CheckModule $_}

# Save the function definitions to run in parallel loops
$GetVCoresDef = $function:GetVCores.ToString()

# Create a script file with the SQL server discovery logic
New-Item  -ItemType file -path DiscoverSql.ps1 -value $function:DiscoveryOnWindows.ToString() -Force | Out-Null
New-Item  -ItemType file -path DiscoverSql.sh -value $DiscoveryOnLinux -Force | Out-Null

# Subscriptions to scan


if ($SubId -like "*.csv") {
    $subscriptions = Import-Csv $SubId
}elseif($SubId.length -gt 0){
    $subscriptions = [PSCustomObject]@{SubscriptionId = $SubId} | Get-AzSubscription
}else{
    $subscriptions = Get-AzSubscription
}


#File setup
if (!$PSBoundParameters.ContainsKey("FilePath")) {
    $FilePath = '.\sql-vm-inventory.csv'
}

[System.Collections.ArrayList]$inventoryTable = @()
$inventoryTable += ,(@("Subscription Name", "Subscription ID", "ResourceGroupName", "Name", "Location", "SKU", "vCores", "OS Type", "OS Version", "SQL Version", "SQL Edition", "IaaS registration"))

$global:VM_SKUs = @{} # To hold the VM SKU table for future use

Write-Host ([Environment]::NewLine + "-- Scanning subscriptions --")

# Calculate usage for each subscription

foreach ($sub in $subscriptions){

    if ($sub.State -ne "Enabled") {continue}

    try {
        Set-AzContext -SubscriptionId $sub.Id
    }catch {
        write-host "Invalid subscription: " $sub.Id
        {continue}
    }

    # Reset the subtotals
    #$subtotal.psobject.properties.name | Foreach-object {$subtotal.$_ = 0}

    # Get all resource groups in the subscription
    #$rgs = Get-AzResourceGroup

    # Scan all VMs with SQL server installed using a parallel loop (up to 10 at a time).
    # NOTE: ForEach-Object -Parallel requires PS v7.1 or higher
    if ($PSVersionTable.PSVersion.Major -ge 7){
        #Get-AzVM -Status | Where-Object { $_.powerstate -eq 'VM running' } | ForEach-Object -ThrottleLimit 10 -Parallel {
        Get-AzVM -Status | Where-Object { $_.powerstate -eq 'VM running' } | ForEach-Object {
            #$function:GetVCores = $using:GetVCoresDef
            $SqlEdition = ''
            $SqlVersion = ''
            $vCores = GetVCores -type 'virtualMachines' -name $_.HardwareProfile.VmSize
            $sql_vm = Get-AzSqlVm -ResourceGroupName $_.ResourceGroupName -Name $_.Name -ErrorAction Ignore


            if ($sql_vm) {
                $RegStatus = 'SQL Server registered'
                $SqlEdition = $Sql_vm.Sku
                $SqlVersion = $Sql_vm.Offer
            }
            else {
               if ($_.StorageProfile.OSDisk.OSType -eq "Windows"){
                    $params =@{
                        ResourceGroupName = $_.ResourceGroupName
                        Name = $_.Name
                        CommandId = 'RunPowerShellScript'
                        ScriptPath = 'DiscoverSql.ps1'
                        ErrorAction = 'Stop'
                    }
                }
                else {
                    $params =@{
                        ResourceGroupName = $_.ResourceGroupName
                        Name = $_.Name
                        CommandId = 'RunShellScript'
                        ScriptPath = 'DiscoverSql.sh'
                        ErrorAction = 'Stop'
                    }
                }
                try {
                    $out = Invoke-AzVMRunCommand @params
                    if (!$out.Value[0].Message){
                        $RegStatus = 'SQL Server not installed'
                    }
                    else {
                        $SqlVersion, $SqlEdition = $out.Value[0].Message -split ':', 2
                        $RegStatus = 'SQL Server not registered'
                    }
                }
                catch {
                    $RegStatus = 'No VM access'
                }
            }
            $inventoryTable += ,(@( $sub.Name, $sub.Id, $_.ResourceGroupName, $_.Name, $_.Location, $_.HardwareProfile.VmSize, $vCores, $_.StorageProfile.ImageReference.Offer, $_.StorageProfile.ImageReference.Sku, $SqlVersion, $SqlEdition, $RegStatus))
            #write-host $_.ResourceGroupName $_.Name $_.Location $_.HardwareProfile.VmSize $vCores $_.StorageProfile.ImageReference.Offer $_.StorageProfile.ImageReference.Sku $SqlVersion $SqlEdition $RegStatus
        }
    }
    [system.gc]::Collect()
}


# Write usage data to the .csv file
if ($FilePath){
    (ConvertFrom-Csv ($inventoryTable | %{$_ -join ','})) | Export-Csv $FilePath -NoType #-Append
    Write-Host ([Environment]::NewLine + "-- Added the usage data to $FilePath --")
} else {
    Write-Host $inventoryTable
}

