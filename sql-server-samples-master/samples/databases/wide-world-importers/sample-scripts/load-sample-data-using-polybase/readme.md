# Load World Wide Importers data into a data warehouse using Polybase and blob storage

This script shows how to load data from Azure Blob storage to Azure SQL Data Warehouse using Polybase. It loads the Wide World Importers dataset into an existing empty SQL Data Warehouse. To follow the script step-by-step in tutorial format, see [Tutorial: Load data to Azure SQL Data Warehouse](https://docs.microsoft.com/azure/sql-data-warehouse/load-data-wideworldimportersdw)

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
1. **Applies to:** Azure SQL Data Warehouse
2. **Key features:** Polybase, data loading
3. **Programming Language:** T-SQL
4. **Authors:** Casey Karst, Barbara Kress, Ayo Olubeko
5. **Update history:** 6 April 2018 - initial revision

<a name=before-you-begin></a>

## Before you begin

To run this sample, you need the following prerequisites.

**Software prerequisites:**

* SQL Server Management Studio (SSMS), or Visual Studio 2015 (or higher) with the latest SSDT installed.

**Azure prerequisites:**

* An existing empty Azure SQL data warehouse

**Data warehouse prerequisites:**

* Login and user that is dedicated for loading data. For more details on how to do this, see [Create a user for loading data](https://docs.microsoft.com/azure/sql-data-warehouse/load-data-wideworldimportersdw#create-a-user-for-loading-data)

<a name=run-this-sample></a>

## Running the sample

1. Open Visual Studio or SSMS and connect to your data warehouse using the login dedicated for loading data.
2. Execute the  T-SQL script
3. Run analytics queries on your data warehouse

## Sample details

The script does the following tasks to load the World Wide Importers sample dataset into your data warehouse:

* Creates external tables that use Azure blob as the data source
* Uses the CTAS T-SQL statement to load data into the data warehouse
* Creates a stored procedure to generate a year of data in the date dimension and sales fact tables
* Creates statistics on the newly loaded data

<a name=disclaimers></a>

## Disclaimers
The code included in this sample is not intended to be used for production purposes.

<a name=related-links></a>

## Related Links
<!-- Links to more articles. Remember to delete "en-us" from the link path. -->
For more information, see these articles:
- [Tutorial: Load data into Azure SQL DataWarehouse](https://docs.microsoft.com/azure/sql-data-warehouse/load-data-wideworldimportersdw)
- [ELT Data Loading Overview](https://docs.microsoft.com/azure/sql-data-warehouse/design-elt-data-loading)
- [Best practices for loading data into Azure SQL DataWarehouse](https://docs.microsoft.com/azure/sql-data-warehouse/guidance-for-loading-data)
