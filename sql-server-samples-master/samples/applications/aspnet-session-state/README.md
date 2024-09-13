# ASP.NET Session State with SQL Server In-Memory OLTP
ASP.NET session state enables you to store and retrieve values for a user as the user navigates the different ASP.NET pages that make up a Web application. Currently, ASP.NET ships with three session state providers that provide the interface between Microsoft ASP.NET’s session state module and session state data sources:
- InProcSessionStateStore, which stores session state in memory in the ASP.NET worker process
- OutOfProcSessionStateStore, which stores session state in memory in an external state server process
- **SqlSessionStateStore**, which stores session state in Microsoft SQL Server database

We are focusing on the SqlSessionStateStore provider and describe how you can configure it to use SQL Server In-Memory OLTP as the storage option for session data. You can either use the [latest ASP.NET async version of the SQL Session State provider](https://www.nuget.org/packages/Microsoft.AspNet.SessionState.SqlSessionStateProviderAsync/) **(which is the recommended approach)**, or configure an earlier version of the provider to work with In-Memory OLTP by downloading and running the In-Memory OLTP SQL scripts from our sql server samples github repo.

Please visit this blog post: https://blogs.msdn.microsoft.com/sqlserverstorageengine/2017/11/28/asp-net-session-state-with-sql-server-in-memory-oltp/ for details on how you can get started.

### Contents

[About this sample](#about-this-sample)<br/>
[Before you begin](#before-you-begin)<br/>
[Install scripts](#install-scripts)<br/>
[Disclaimers](#disclaimers)<br/>
[Related links](#related-links)<br/>

<a name=about-this-sample></a>

## About this sample

1. **Applies to:** SQL Server 2016 (or higher) Enterprise / Developer / Evaluation Edition, Azure SQL Database (Premium)
2. **Key features:**
	- ASP.NET Session State Provider
	- Memory Optimized Tables
	- Natively Compiled Stored Procedures
4. **Programming Language:** T-SQL
5. **Authors:** Perry Skountrianos [perrysk-msft]

<a name=before-you-begin></a>

## Before you begin

**Software prerequisites:**

1. SQL Server 2016 (or higher) Enterprise / Developer / Evaluation Edition or Azure SQL Database (Premium)
2. .NET Framework 2.0 or higher

<a name=install-scripts></a>

## T-SQL Scripts
There are two versions of the SQL Server script (with retry logic and without):

-   [aspstate_sql2016 (no retry logic)](https://github.com/Microsoft/sql-server-samples/blob/master/samples/applications/aspnet-session-state/aspstate_sql2016_no_retry.sql)
-   [aspstate_sql2016 (with retry logic)](https://github.com/Microsoft/sql-server-samples/blob/master/samples/applications/aspnet-session-state/aspstate_sql2016_with_retry.sql)

Based on your workload characteristics and the way your application handles session state you have to decide if retry logic is needed or not. [This](https://msdn.microsoft.com/en-us/library/mt668435.aspx) article explains the logic used to detect conflict and implement retry logic in the script. Currently, the two memory-optimized tables:  **dbo.ASPStateTempApplications** and **dbo.ASPStateTempSessions** in both of the scripts are created with **DURABILITY = SCHEMA_ONLY** meaning that in a case of a SQL Server restart or a reconfiguration occurs in an Azure SQL Database, the table schema persists, but data in the table is lost. If durability of both schema and data is required tthe script needs to be altered and the two tables above need to be created with: **DURABILITY=SCHEMA\_AND\_DATA**.[This](https://msdn.microsoft.com/en-us/library/dn553122.aspx) article explains the two durability options for memory-optimized tables

<a name=sample-details></a>

## Disclaimers
The code included in this sample is not intended to be a set of best practices on how to build scalable enterprise grade applications. This is beyond the scope of this quick start sample.

<a name=related-links></a>

## Related Links
<!-- Links to more articles. Remember to delete "en-us" from the link path. -->

For more information, see these articles:

- [In-Memory OLTP (In-Memory Optimization)](https://msdn.microsoft.com/en-us/library/dn133186.aspx)
- [OLTP and database management](https://www.microsoft.com/en-us/sql-server/oltp-database-management)
- [Session State Provider](https://msdn.microsoft.com/en-us/library/aa478952.aspx)
- [Implementing a Session-State Store Provider](https://msdn.microsoft.com/en-us/library/ms178587.aspx)
