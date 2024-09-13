-- Create database scoped credential to connect to MySQL server
-- Provide appropriate credentials to MySQL server in below statement.
-- If you are using SQL Server Management Studio then you can replace the parameters using
-- the Query menu, and "Specify Values for Template Parameters" option.
IF NOT EXISTS(SELECT * FROM sys.database_scoped_credentials WHERE name = 'MySQL80-user')
  CREATE DATABASE SCOPED CREDENTIAL [MySQL80-user]
  WITH IDENTITY = '<mysql_user,nvarchar(100),mssql-user>'
  , SECRET = '<mysql_user_password,nvarchar(100),sql19tw0mysql>';

-- Create external data source that points to MySQL server.
--
IF NOT EXISTS(SELECT * FROM sys.external_data_sources WHERE name = 'MySQL80')
    CREATE EXTERNAL DATA SOURCE MySQL80
    WITH (LOCATION = 'odbc://<mysql_server,nvarchar(100),mysql-server-name>'
    , CONNECTION_OPTIONS = 'Driver={MySQL ODBC 8.0 Unicode Driver};IGNORE_SPACE=1'
    , CREDENTIAL = [MySQL80-user]);

-- Create external table over inventory table on MySQL server
--
IF NOT EXISTS(SELECT * FROM sys.external_tables WHERE name = 'mysql_version')
    CREATE EXTERNAL TABLE mysql_version
	(
	[sys_version] NVARCHAR(5) NOT NULL,
	[mysql_version] NVARCHAR(6) NOT NULL
	)
    WITH (LOCATION = 'sys.version', DATA_SOURCE = MySQL80);

SELECT * FROM mysql_version;

/*
IF NOT EXISTS(SELECT * FROM sys.external_tables WHERE name = 'mysql_tables')
    CREATE EXTERNAL TABLE mysql_tables
    (
		TABLE_CATALOG	nvarchar(64),	
		TABLE_SCHEMA	nvarchar(64),		
		TABLE_NAME	nvarchar(64),	
		TABLE_TYPE	nvarchar(64),		
		ENGINE	nvarchar(64),		
		VERSION	smallint,			
		ROW_FORMAT	nvarchar(64),		
		TABLE_ROWS	bigint,
		AVG_ROW_LENGTH	bigint,			
		DATA_LENGTH	bigint,			
		MAX_DATA_LENGTH	bigint,			
		INDEX_LENGTH	bigint,			
		DATA_FREE	bigint,			
		AUTO_INCREMENT	bigint,			
		CREATE_TIME	datetime2,		
		UPDATE_TIME	datetime2,
		CHECK_TIME	datetime2,
		TABLE_COLLATION	nvarchar(64),
		CHECKSUM	bigint,
		CREATE_OPTIONS	nvarchar(256),
		TABLE_COMMENT	nvarchar(256)
    )
    WITH (LOCATION = 'information_schema.tables', DATA_SOURCE = MySQL80);

SELECT * FROM mysql_tables;
*/
-- Cleanup
/*
DROP EXTERNAL TABLE mysql_version
DROP EXTERNAL TABLE mysql_tables
DROP EXTERNAL DATA SOURCE MySQL80
DROP DATABASE SCOPED CREDENTIAL [MySQL80-user]
*/
