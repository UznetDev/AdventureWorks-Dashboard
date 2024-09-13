# Upload certificate to Azure SQL Managed Instance using Azure PowerShell

Script that takes path to .cer and .pvk files and uploads them to SQL MI. See [more](https://docs.microsoft.com/en-us/azure/sql-database/sql-database-managed-instance-migrate-tde-certificate).

### Contents

[About this sample](#about-this-sample)<br/>
[Before you begin](#before-you-begin)<br/>
[Run this sample](#run-this-sample)<br/>
[Sample details](#sample-details)<br/>
[Disclaimers](#disclaimers)<br/>
[Related links](#related-links)<br/>


<a name=about-this-sample></a>

## About this sample

- **Applies to:** Azure SQL Database
- **Key features:**  Managed Instance
- **Workload:** n/a
- **Programming Language:** PowerShell
- **Authors:** Srdan Bozovic
- **Update history:** n/a

<a name=before-you-begin></a>

## Before you begin

To run this sample, you need the following prerequisites.

**Software prerequisites:**

1. Running Microsoft Windows operating system (as script uses PInvoke for crypto api)
2. PowerShell 5.0 or higher installed
3. AzureRM.Sql module version 4.10.0 or higher

**Azure prerequisites:**

1. Permission to manage Azure SQL Managed Instance

<a name=run-this-sample></a>

## Run this sample

Run the script below from either Windows or Azure Cloud Shell

```powershell

$scriptUrlBase = 'https://raw.githubusercontent.com/Microsoft/sql-server-samples/master/samples/manage/azure-sql-db-managed-instance/upload-tde-certificate'

$parameters = @{
    subscriptionId = '<subscriptionId>'
    resourceGroupName = '<resourceGroupName>'
    managedInstanceName  = '<managedInstanceName>'
    publicKeyFile  = '<publicKeyFile>'
    privateKeyFile  = '<privateKeyFile>'
    password  = '<password>'
    }

Invoke-Command -ScriptBlock ([Scriptblock]::Create((iwr ($scriptUrlBase+'/uploadTDECertificate.ps1?t='+ [DateTime]::Now.Ticks)).Content)) -ArgumentList $parameters

```

<a name=sample-details></a>

## Sample details

This sample shows how to convert .cer and .pvk files to base64 .pfx blob and upload it to SQL MI using PowerShell.

<a name=disclaimers></a>

## Disclaimers
The scripts and this guide are copyright Microsoft Corporations and are provided as samples. They are not part of any Azure service and are not covered by any SLA or other Azure-related agreements. They are provided as-is with no warranties express or implied. Microsoft takes no responsibility for the use of the scripts or the accuracy of this document. Familiarize yourself with the scripts before using them.

<a name=related-links></a>

## Related Links
<!-- Links to more articles. Remember to delete "en-us" from the link path. -->

For more information, see these articles:

- [What is a Managed Instance (preview)?](https://docs.microsoft.com/azure/sql-database/sql-database-managed-instance)
- [Configure a VNet for Azure SQL Database Managed Instance](https://docs.microsoft.com/azure/sql-database/sql-database-managed-instance-vnet-configuration)