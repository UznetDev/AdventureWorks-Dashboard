# ETL Process for WideWorldImporters

This SSIS project performs ETL from the transactional database WideWorldImporters into the OLAP database WideWorldImportersDW for long-term storage and analytics.

### Contents

[About this sample](#about-this-sample)<br/>
[Before you begin](#before-you-begin)<br/>
[Running the sample](#run-this-sample)<br/>
[Sample details](#sample-details)<br/>
[Disclaimers](#disclaimers)<br/>
[Related links](#related-links)<br/>


<a name=about-this-sample></a>

## About this sample

<!-- Delete the ones that don't apply -->
1. **Applies to:** SQL Server 2016 (or higher)
1. **Key features:** Core database features
1. **Workload:** ETL
1. **Programming Language:**
1. **Authors:** Greg Low, Denzil Ribeiro, Jos de Bruijn
1. **Update history:** 25 May 2016 - initial revision

<a name=before-you-begin></a>

## Before you begin

To run this sample, you need the following prerequisites.

**Software prerequisites:**

1. The databases WideWorldImporters and WideWorldImportersDW running on SQL Server 2016 (or higher) or Azure SQL Database. These can be on different servers.
2. Visual Studio 2015 Update 3 (or higher). At the time of writing, Visual Studio 2017 does not yet support Integration Services projects. You will need to install Visual Studio 2015 to open the SSIS project.
3. SQL Server 2016 (or higher) Integration Services.
    1. This needs to be installed on the same machine as Visual Studio to be able to build the project.
    1. Make sure you have already created an SSIS Catalog. If not, to do that, right click Integration Services in Object Explorer, and choose to add catalog. Follow the defaults. It will ask you to enable sqlclr and provide a password.

<a name=run-this-sample></a>

## Running the sample

1. Open the solution file wwi-ssis.sln in Visual Studio.

2. Build the solution. This will create an SSIS package **Daily ETL.ispac** under Daily ETL\\bin\\Development.

3. Deploy the SSIS package.
    1. Open the "Daily ETL.ispac" package from Windows Explorer. This will launch the Integration Services Deployment Wizard.
    1. Under "Select Source" follow the default Project Deployment, with the path pointing to the "Daily ETL.ispac" package.
    1. Under "Select Destination" enter the name of the server that hosts the SSIS catalog.
    1. Select a path under the SSIS catalog, for example under a new folder "WideWorldImporters".
    1. Finalize the wizard by clicking Deploy.

4. Create a SQL Server Agent job for the ETL process.
    1. In SSMS, right-click "SQL Server Agent" and select New->Job.
    1. Pick a name, for example "WideWorldImporters ETL".
    1. Add a Job Step of type "SQL Server Integration Services Package".
       - Select the server with the SSIS catalog, and select the "Daily ETL" package.
       - Under Configuration->Connection Managers ensure the connections to the source and target are configured correctly. The default is to connect to the local instance.
    1. Click OK to create the Job.

5. Execute or schedule the Job.

## Sample details

The ETL package **Daily ETL.ispac** is used to migrate data from the WideWorldImporters database to the WideWorldImportersDW database as the data changes. The package is run periodically (most commonly daily).

The design of the package uses SSIS to orchestrate bulk T-SQL operations (rather than as separate transformations within SSIS) to ensure high performance.

Dimensions are loaded first, followed by Fact tables. The package can be re-run at any time after a failure.

The workflow is as follows:

![Alt text](/media/wide-world-importers-etl-workflow.png "WideWorldImporters ETL Workflow")

It starts with an expression task that works out the appropriate cutoff time. This time is the current time less a few seconds. (This is more robust than requesting data right to the current time). It then truncates any milliseconds from the time.

The main processing starts by populating the Date dimension table. It ensures that all dates for the current year have been populated in the table.

After this, a series of data flow tasks loads each dimension, then each fact.


<a name=disclaimers></a>

## Disclaimers
The code included in this sample is not intended to be used for production purposes.

<a name=related-links></a>

## Related Links
For more information, see these articles:
- [SQL Server Integration Services documentation](https://msdn.microsoft.com/library/ms141026.aspx)
