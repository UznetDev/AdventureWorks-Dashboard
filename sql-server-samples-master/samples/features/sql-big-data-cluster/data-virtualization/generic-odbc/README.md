# Data virtualization in SQL Server 2019

***Applies to:*** SQL Server 2019 on Windows only

SQL Server 2019 introduces new ODBC connectors to data sources like SQL Server, Oracle, MongoDB and Teradata. The generic ODBC
connector can also be used to connect to other data sources like PostgreSQL, MySQL, IBM DB2 or any data source that provides
an ODBC driver. The ability to use the generic ODBC connector from SQL Server will be available only on Windows platform.

The steps to use the generic ODBC connector are:

1. Install the 64-bit ODBC Driver for the data source (ex: PostgreSQL, MySQL, IBM DB2, SAP HANA) on the SQL Server machine
1. Installation of the ODBC driver should be done at the system level
1. Use the Windows Control Panel ODBC applet (odbcad32) to determine the name of the ODBC Driver or refer to the ODBC Driver documentation

## Query data in PostgreSQL from SQL Server

In this example, you are going to create an external table in a SQL Server 2019 instance on Windows over the pg_tables view that sits on a PostgreSQL 11 server. The driver used to connect to the PostgreSQL server was the ***PostgreSQL ODBC Driver(UNICODE)*** driver.

**Before you begin**, you need to have the PostgreSQL instance name and credentials

### Instructions

1. Connect to a SQL Server 2019 Windows instance and database.

1. Modify the parameters in [postgresql/pg_tables.sql](postgresql/pg_tables.sql/).

1. Execute the SQL [postgresql/pg_tables.sql](postgresql/pg_tables.sql/).

## Query data in MySQL from SQL Server

In this example, you are going to create an external table in a SQL Server instance on Windows over the pg_tables view that sits on a MySQL 8.0 server. The driver used to connect to the MySQL server was the ***MySQL 8.0 ODBC Driver Unicode Driver*** driver.

**Before you begin**, you need to have the PostgreSQL instance name and credentials

### Instructions

1. Connect to a SQL Server 2019 Windows instance and database.

1. Modify the parameters in [mysql/mysql_version.sql](mysql/mysql_version.sql/).

1. Execute the SQL [mysql/mysql_version.sql](mysql/mysql_version.sql/).
