# Data virtualization in SQL Server 2019 and SQL Server 2019 big data cluster

In **SQL Server 2019 big data clusters**, the SQL Server engine has gained the ability to natively read HDFS files, such as CSV and parquet files, by using SQL Server instances collocated on each of the HDFS data nodes to filter and aggregate data locally in parallel across all of the HDFS data nodes. **SQL Server 2019** also introduces **new ODBC connectors** to data sources like SQL Server, Oracle, MongoDB and Teradata.

## Query data in HDFS from SQL Server master

**Applies to: SQL Server 2019 big data cluster**

In SQL Server 2019 big data cluster, the storage pool consists of HDFS data node with SQL Server & Spark endpoints. The [storage-pool](storage-pool) folder contains SQL scripts that demonstrate how to query data residing in HDFS data inside a big data cluster. The [hadoop](hadoop) folder contains SQL scripts that demonstrate how to query data residing in HDFS data using the HADOOP data source for
operations that are not yet supported with storage pool (ex: export data to HDFS).

## Query data in Oracle from SQL Server master

**Applies to: SQL Server 2019 on Windows or Linux, SQL Server 2019 big data cluster**

The [oracle](oracle) folder contains SQL scripts that demonstrate how to query data residing in Oracle instance.
