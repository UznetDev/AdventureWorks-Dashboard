# WideWorldImportersDW OLAP Database

The Visual Studio SQL Server Data Tools project in this folder is used to construct the WideWorldImportersDW database from scratch on SQL Server or Azure SQL Database. It is possible to vary the data size.

A pre-created version of the database is available for download as part of the latest release of the sample: [wide-world-importers-release](https://aka.ms/wwi).

### Contents

[About this sample](#about-this-sample)<br/>
[Before you begin](#before-you-begin)<br/>
[Run this sample](#run-this-sample)<br/>
[Disclaimers](#disclaimers)<br/>

<a name=about-this-sample></a>

## About this sample

<!-- Delete the ones that don't apply -->
1. **Applies to:** SQL Server 2016 (or higher), Azure SQL Database
1. **Key features:** Core database features
1. **Workload:** OLTP
1. **Programming Language:** Transact-SQL
1. **Authors:** Greg Low, Denzil Ribeiro, Jos de Bruijn, Robert Cain

The instructions below are for creating the sample database from scratch.

<a name=before-you-begin></a>

## Before you begin

To run this sample, you need the following prerequisites.

**Software prerequisites:**

1. SQL Server 2016 SP1 (or higher) or an Azure SQL Database (Premium). Also works with SQL Server 2016 RTM, for Evaluation, Developer, and Enterprise edition.
2. Visual Studio 2015 Update (or higher) with SQL Server Data Tools (SSDT). We recommend you update to the latest available of SSDT from the Visual Studio Extensions and Updates feed.


<a name=run-this-sample></a>

## Run this sample

The below steps reconstruct the WideWorldImportersDW database. To populate the database, you need to have the WideWorldImporters database as well.

<!-- Step by step instructions. Here's a few examples -->

### Publishing to SQL Server

1. Open the solution **wwi-dw-ssdt.sln** in Visual Studio. Skip this step if you have already opened the solution **wwi-sample.sln** in the root of this sample.

2. Build the solution.

3. Publish the WideWorldImportersDW database:
    1. In the Solution Explorer, right-click the **WideWorldImportersDW** project, and select **Publish** to bring up the **Publish Database** dialog.
    1. Click **Edit** to modify the **Target Database Connection** to point to your SQL Server.
    1. Edit the **Database Name** to "WideWorldImportersDW".
    1. Click **Publish**.
    1. Wait for the publication process to finish. You can monitor progress in the **Data Tools Operations** page in Visual Studio. During testing this took around 3 minutes.

4. Execute the SQL Server Integration Services package **Daily ETL** once, to seed the WideWorldImportersDW database based on the contents of the WideWorldImporters database. For instructions on how to install and run this package see [wwi-ssis] (../wwi-ssis/).


### Publishing to Azure SQL Database

To publish the database to Azure SQL Database, complete the following steps after Step 1 in the previous section:

A. Update the partition scheme `Storage\PS_Date.sql` as follows: replace every occurrence of `USERDATA` with `PRIMARY`.<br/>
B. Delete the filegroups `Storage\USERDATA.sql` and `Storage\WWI_MemoryOptimized_Date.sql`.<br/>
C. Right-click the project **WideWorldImportersDW** and select **Properties** to open the properties pane.<br/>
D. Change the **Target Platform** to **Microsoft Azure SQL Database v12**, and press **Ctrl-S** to save.<br/>
E. Create a new Azure SQL Database with the name WideWorldImportersDW. As pricing tier, select **Premium**. For instructions see: [Create an Azure SQL database in the Azure portal](https://docs.microsoft.com/azure/sql-database/sql-database-get-started-portal).

Continue with Step 2 above.

<a name=disclaimers></a>

## Disclaimers
The code included in this sample is not intended to be used for production purposes.
