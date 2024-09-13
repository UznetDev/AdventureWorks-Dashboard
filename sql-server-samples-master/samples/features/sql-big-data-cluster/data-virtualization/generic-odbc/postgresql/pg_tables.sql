-- Create database scoped credential to connect to PostgreSQL server
-- Provide appropriate credentials to PostgreSQL server in below statement.
-- If you are using SQL Server Management Studio then you can replace the parameters using
-- the Query menu, and "Specify Values for Template Parameters" option.
IF NOT EXISTS(SELECT * FROM sys.database_scoped_credentials WHERE name = 'PostgreSQL11-user')
  CREATE DATABASE SCOPED CREDENTIAL [PostgreSQL11-user]
  WITH IDENTITY = '<postgres_user,nvarchar(100),mssql-user>'
  , SECRET = '<postgres_user_password,nvarchar(100),sql19tw0postgresql>';

-- Create external data source that points to PostgreSQL server.
--
IF NOT EXISTS(SELECT * FROM sys.external_data_sources WHERE name = 'PostgreSQL11')
    CREATE EXTERNAL DATA SOURCE PostgreSQL11
    WITH (LOCATION = 'odbc://<postgres_server,nvarchar(100),postgres-server-name>'
    , CONNECTION_OPTIONS = 'Driver={PostgreSQL ODBC Driver(UNICODE)}'
    , CREDENTIAL = [PostgreSQL11-user]);

-- Create external table over inventory table on PostgreSQL server
--
IF NOT EXISTS(SELECT * FROM sys.external_tables WHERE name = 'pg_tables')
    CREATE EXTERNAL TABLE pg_tables
    (
        schemaname nvarchar(128) not null,
        tablename nvarchar(128) not null,
        tableowner nvarchar(128) not null,
        tablespace nvarchar(128) not null,
        hasindexes nvarchar(5) not null,
        hasrules nvarchar(5) not null,
        hastriggers nvarchar(5) not null,
        rowsecurity nvarchar(5) not null
    )
    WITH (LOCATION = 'postgres.pg_catalog.pg_tables', DATA_SOURCE = PostgreSQL11);

SELECT * FROM pg_tables;

-- Cleanup
/*
DROP EXTERNAL TABLE pg_tables
DROP EXTERNAL DATA SOURCE PostgreSQL11
DROP DATABASE SCOPED CREDENTIAL [PostgreSQL11-user]
*/
