# Power BI Reports for Consolidated Migration Assessments

This contains examples of Power BI reports for consolidated migration assessements. The assessments are generated using Data Migration Assistant, to evaluate moving data to SQL Server or to Azure SQL Database.


### Contents

[About this sample](#about-this-sample)<br/>
[Before you begin](#before-you-begin)<br/>
[Run this sample](#run-this-sample)<br/>
[Sample details](#sample-details)<br/>
[Related links](#related-links)<br/>


<a name=about-this-sample></a>

## About this sample


- **Applies to:** SQL Server 2016 (or higher), Azure SQL Database
- **Key features:** Migration assessments


<a name=before-you-begin></a>

## Before you begin

To run this sample, you need the following prerequisites.

**Software prerequisites:**

1. Power BI
2. SQL Server 2016 (or higher) or an Azure SQL Database
3. Data Migration Assistant

**Azure prerequisites:**

1. Permission to create an Azure SQL Database

<a name=run-this-sample></a>

## Run this sample

<!-- Step by step instructions. Here's a few examples -->

1. Copy the DMA Reports V3.1.pbix file locally.
2. Open the file using Power BI.

<a name=sample-details></a>

## Sample details

This includes the following Power BI reports, for consolidated migration assessments.
- **Dashboard:** Provides snapshot stats and a drill down report.
- **On Premise Upgrade Readiness:** Shows the percentage upgrade success for you assessed databases.
- **On Premise Feature Parity Report -- Details:** Highlights new features that can be used for database in the target SQL Server version.
- **Azure SQL DB Upgrade Readiness:** Shows the percentage upgrade success for databases assessed for Azure SQL DB migrations.
- **Azure SQL DB Unsuppported Features:** Shows features that in your existing databases are not supported in Azure SQL DB (v12).

<a name=related-links></a>

## Related Links

For more information, see these articles:

[Report on your Consolidated Assessments using Power BI (Data Migration Assistant)](https://docs.microsoft.com/sql/dma/dma-powerbiassesreport)