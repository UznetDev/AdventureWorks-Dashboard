--=====================================
-- Attach database template
--=====================================
IF NOT EXISTS(
  SELECT *
    FROM sys.databases
   WHERE name = N'<database_name, sysname, your_database_name>'
)
	CREATE DATABASE <database_name, sysname, your_database_name>
		ON PRIMARY (FILENAME = '<database_primary_file_path,,C:\Program files\Microsoft SQL Server\%INST_PRE%.MSSQLSERVER\MSSQL\Data\your_database_name.MDF>')
		FOR ATTACH
GO
