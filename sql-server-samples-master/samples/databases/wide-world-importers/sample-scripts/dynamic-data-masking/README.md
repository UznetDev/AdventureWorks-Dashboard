# Sample for use of Dynamic Data Masking in WideWorldImporters

This script demonstrates the use of Dynamic Data Masking to mask sensitive data for certain users.


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
1. **Applies to:** SQL Server 2016 (or higher), Azure SQL Database
1. **Key features:** Dynamic Data Masking
1. **Workload:** OLTP
1. **Programming Language:** T-SQL
1. **Author:** Rick Davis
1. **Update history:** 20 October 2016 - initial revision

<a name=before-you-begin></a>

## Before you begin

To run this sample, you need the following prerequisites.

**Software prerequisites:**

<!-- Examples -->
1. SQL Server 2016 (or higher) or Azure SQL Database.
 - With SQL Server, make sure SQL authentication is enabled.
2. SQL Server Management Studio
3. The WideWorldImporters database.

<a name=run-this-sample></a>

## Running the sample

1. Open the script DemonstrateDDM.sql in Management Studio and connect to the WideWorldImporters database.

2. Follow the instructions in the script.

## Sample details

The WideWorldImporters sample database leverages Dynamic Data Masking to mask sensitive banking data in the table 'Purchasing.Suppliers'.

When connecting to the database and running a query using a privileged user such as the database owner, you will see the sensitive data in the clear.

The user 'GreatLakesSales' is an example unprivileged user, and will only see the masked values.

<a name=disclaimers></a>

## Disclaimers
The code included in this sample is not intended to be used for production purposes.

<a name=related-links></a>

## Related Links
For more information, see these articles:
- [Row-Level Security documentation](https://msdn.microsoft.com/library/dn765131.aspx)
- [Row-Level Security SQL Server 2016 (video)](https://channel9.msdn.com/Events/DataDriven/SQLServer2016/Row-Level-Security)
