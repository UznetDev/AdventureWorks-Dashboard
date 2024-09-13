# WideWorldImporters Sample Database for SQL Server and Azure SQL Database

WideWorldImporters is a sample for SQL Server and Azure SQL Database. It showcases database design, as well as how to best leverage SQL Server features in a database.

WideWorldImporters is a wholesale company. Transactions and real-time analytics are performed in the database WideWorldImporters. The database WideWorldImportersDW is an OLAP database, focused on analytics.

The sample includes the databases that can be explored, as well as sample applications and sample scripts that can be used to explore the use of individual SQL Server features in the sample database.

**Latest release**: [wide-world-importers-release](http://go.microsoft.com/fwlink/?LinkID=800630)

**Documentation**: [Wide World Importers Documentation](http://go.microsoft.com/fwlink/?LinkID=800631)

**Feedback on the sample**: send to [sqlserversamples@microsoft.com](mailto:sqlserversamples@microsoft.com)

### Contents

[About this sample](#about-this-sample)<br/>
[Before you begin](#before-you-begin)<br/>
[Sample structure](#run-this-sample)<br/>
[Disclaimers](#disclaimers)<br/>
[Related links](#related-links)<br/>


<a name=about-this-sample></a>

## About this sample

<!-- Delete the ones that don't apply -->
1. **Applies to:** SQL Server 2016 (or higher), Azure SQL Database
1. **Key features:** Core database features
1. **Workload:** OLTP, OLAP, IoT
1. **Programming Language:** T-SQL, C#
1. **Authors:** Greg Low, Denzil Ribeiro, Jos de Bruijn, Robert Cain
1. **Update history:**
	21 June 2017 - restructure using SSDT
	25 May 2016 - initial revision


<a name=before-you-begin></a>

## Before you begin

To run this sample, you need the following prerequisites.

**Software prerequisites:**

<!-- Examples -->
1. SQL Server 2016 (or higher) or an Azure SQL Database.
1. SQL Server Management Studio, preferably June 2016 release or later (version >= 13.0.15000.23).
1. Visual Studio 2015 Update 3 (or higher) with SQL Server Data Tools.
1. (to run ETL jobs) SQL Server 2016 (or higher) Integration Services (SSIS). At the time of writing, Visual Studio 2017 does not yet support Integration Services projects. You will need to install Visual Studio 2015 to open the SSIS project.
1. (to install the SSASMD sample) SQL Server 2016 (or higher) Analysis Services (SSAS). If you are using Visual Studio 2017, download and install the following: [Analysis Services](https://marketplace.visualstudio.com/items?itemName=ProBITools.MicrosoftAnalysisServicesModelingProjects)

<a name=run-this-sample></a>

## Sample structure

The latest release of this sample is available here: [wide-world-importers-release](http://go.microsoft.com/fwlink/?LinkID=800630)

This sample contains databases as well as a number of sample scripts and workload drivers.

The sample databases are created through SQL Server Data Tools projects in Visual Studio. Each database has its own project; the solution [wwi-sample.sln](wwi-sample.sln) in the root folder of the sample has references to all the projects. To load all project in the solution, SQL Server Integration Services and SQL Server Analysis Services need to be installed on the machine.

The sample scripts are available as Transact-SQL. The workload drivers are sample applications created in Visual Studio.

The source code for the sample is further structured as follows:

__[power-bi-dashboards](power-bi-dashboards/)__

Sample Power BI dashboards that leverage the WideWorldImporters and WideWorldImportersDW databases.

__[sample-scripts](sample-scripts/)__

Sample scripts that illustrate the use of various SQL Server features with the WideWorldImporters sample database.

__[workload-drivers](workload-drivers/)__

Simple apps that simulate workloads for the WideWorldImporters sample database.

__[wwi-dw-ssdt](wwi-dw-ssdt/)__

SQL Server Data Tools project for the OLAP database WideWorldImporters.

__[wwi-ssasmd](wwi-ssasmd/)__

SQL Server Analysis Services Multidimensional project to create the Analysis Services database WWI-SSASMD.

__[wwi-ssdt](wwi-ssdt/)__

SQL Server Data Tools project for the main OLTP database WideWorldImporters.

__[wwi-ssis](wwi-ssis/)__

SQL Server Integration Services (SSIS) project for the Extract, Transform, and Load (ETL) process that takes data from the transactional database WideWorldImporters and loads it into the WideWorldImportersDW database.



<a name=disclaimers></a>

## Disclaimers
The code included in this sample is not intended to be used for production purposes.

<a name=related-links></a>

## Related Links
<!-- Links to more articles. Remember to delete "en-us" from the link path. -->
For more information, see these articles:
- [SQL Server 2016 product page](https://www.microsoft.com/server-cloud/products/sql-server-2016/)
- [SQL Server 2016 download page](https://www.microsoft.com/evalcenter/evaluate-sql-server-2016)
- [Azure SQL Database product page](https://azure.microsoft.com/services/sql-database/)
- [What's new in SQL Server 2016](https://msdn.microsoft.com/en-us/library/bb500435.aspx)
