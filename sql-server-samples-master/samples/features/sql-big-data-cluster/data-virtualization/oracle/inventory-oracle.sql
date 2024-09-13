USE sales
GO

-- Create database scoped credential to connect to Oracle server
-- Provide appropriate credentials to Oracle server in below statement.
-- If you are using SQL Server Management Studio then you can replace the parameters using
-- the Query menu, and "Specify Values for Template Parameters" option.
IF NOT EXISTS(SELECT * FROM sys.database_scoped_credentials WHERE name = 'OracleCredential')
  CREATE DATABASE SCOPED CREDENTIAL [OracleCredential]
  WITH IDENTITY = '<oracle_user,nvarchar(100),sales>', SECRET = '<oracle_user_password,nvarchar(100),sql19tw0oracle>';

-- Create external data source that points to Oracle server
--
IF NOT EXISTS(SELECT * FROM sys.external_data_sources WHERE name = 'OracleSalesSrvr')
  CREATE EXTERNAL DATA SOURCE [OracleSalesSrvr]
  WITH (LOCATION = 'oracle://<oracle_server,nvarchar(100),oracle-server-name>',CREDENTIAL = [OracleCredential]);

-- Create external table over inventory table on Oracle server
-- NOTE: Table names and column names will use ANSI SQL quoted identifier while querying against Oracle.
--       As a result, the names are case-sensitive so specify the name in the external table definition
--       that matches the exact case of the table and column names in the Oracle metadata.
CREATE EXTERNAL TABLE [inventory_ora]
    ([INV_DATE] DECIMAL(10,0) NOT NULL, [INV_ITEM] DECIMAL(10,0) NOT NULL,
    [INV_WAREHOUSE] DECIMAL(10,0) NOT NULL, [INV_QUANTITY_ON_HAND] DECIMAL(10,0))
WITH (DATA_SOURCE=[OracleSalesSrvr],
      LOCATION='<oracle_service_name,nvarchar(30),xe>.SALES.INVENTORY');
GO

-- Find quantity of certain items from inventory for a specific category
--
SELECT TOP(100) w.w_warehouse_name, i.INV_ITEM, SUM(i.INV_QUANTITY_ON_HAND) as total_quantity
  FROM [inventory_ora] as i
  JOIN item as it
    ON it.i_item_sk = i.INV_ITEM
  JOIN warehouse as w
    ON w.w_warehouse_sk = i.INV_WAREHOUSE
 WHERE it.i_category = 'Movies & TV' and i.INV_ITEM BETWEEN 17401 and 17402 --> get items within specific range
 GROUP BY w.w_warehouse_name, i.INV_ITEM;
GO

-- Cleanup
--
/*
DROP EXTERNAL TABLE [inventory_ora];
DROP EXTERNAL DATA SOURCE [OracleSalesSrvr] ;
DROP DATABASE SCOPED CREDENTIAL [OracleCredential];
*/
