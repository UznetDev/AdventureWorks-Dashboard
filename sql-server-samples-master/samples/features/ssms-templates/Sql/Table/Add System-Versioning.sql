--======================================================
-- Adds temporal system-versioning to the table template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template adds temporal system-versioning to the table
--======================================================

USE <database, sysname, AdventureWorks>
GO

IF OBJECT_ID('<schema_name, sysname, dbo>.<table_name, sysname, sample_table>', 'U') IS NOT NULL
BEGIN
    ALTER TABLE [<schema_name, sysname, dbo>].[<table_name, sysname, sample_table>]
	  ADD <StartColumn_name, sysname, SysStartTime> datetime2(7) GENERATED ALWAYS AS ROW START HIDDEN NOT NULL,
          <EndColumn_name, sysname, SysEndTime> datetime2(7) GENERATED ALWAYS AS ROW END HIDDEN NOT NULL,
          PERIOD FOR SYSTEM_TIME(<StartColumn_name, sysname, SysStartTime>,<EndColumn_name, sysname, SysEndTime>)

	 ALTER TABLE [<schema_name, sysname, dbo>].[<table_name, sysname, sample_table>]
	   SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = [<history_schema_name, sysname, dbo>].[<history_table_name, sysname, sample_table_history>]))
 END
GO
