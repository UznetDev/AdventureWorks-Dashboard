# Prepare subnet for Managed Instance deployment

Script that validates and prepares virtual network and subnet for Managed Instance creation to comply with [networking requirements](https://docs.microsoft.com/azure/sql-database/sql-database-managed-instance-vnet-configuration#requirements).

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

1. PowerShell 5.1
2. Azure PowerShell 5.4.2 or higher

**Azure prerequisites:**

1. Permission to manage Azure virtual network

<a name=run-this-sample></a>

## Run this sample

Run the script below from either Windows or Azure Cloud Shell

```powershell

$scriptUrlBase = 'https://raw.githubusercontent.com/Microsoft/sql-server-samples/master/samples/manage/azure-sql-db-managed-instance/prepare-subnet'

$parameters = @{
    subscriptionId = '<subscriptionId>'
    resourceGroupName = '<resourceGroupName>'
    virtualNetworkName = '<virtualNetworkName>'
    subnetName = '<subnetName>'
    }

Invoke-Command -ScriptBlock ([Scriptblock]::Create((iwr ($scriptUrlBase+'/prepareSubnet.ps1?t='+ [DateTime]::Now.Ticks)).Content)) -ArgumentList $parameters

```

<a name=sample-details></a>

## Sample details

This sample shows how to prepare Azure virtual network and subnet for Managed Instance deployment using PowerShell

This is done in three simple steps:
- Validate - Selected virtual netwok and subnet are validated for Managed Instance networking requirements
- Confirm - User is shown a set of changes that need to be made to prepare subnet for Managed Instance deployment and asked for consent
- Prepare - Virtual network and subnet are configured properly

<a name=disclaimers></a>

## Disclaimers
The scripts and this guide are copyright Microsoft Corporations and are provided as samples. They are not part of any Azure service and are not covered by any SLA or other Azure-related agreements. They are provided as-is with no warranties express or implied. Microsoft takes no responsibility for the use of the scripts or the accuracy of this document. Familiarize yourself with the scripts before using them.

<a name=related-links></a>

## Related Links
<!-- Links to more articles. Remember to delete "en-us" from the link path. -->

For more information, see these articles:

- [What is a Managed Instance (preview)?](https://docs.microsoft.com/azure/sql-database/sql-database-managed-instance)
- [Configure a VNet for Azure SQL Database Managed Instance](https://docs.microsoft.com/azure/sql-database/sql-database-managed-instance-vnet-configuration)