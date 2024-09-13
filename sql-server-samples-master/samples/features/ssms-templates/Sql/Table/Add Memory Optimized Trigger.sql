--======================================================
-- Add Trigger to a Memory Optimized Table Template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template adds a trigger to a memory optimized table.
--======================================================
USE [<database_name, sysname, memory_optimized_database>]
GO

CREATE TRIGGER [<schema_name, , dbo>].[<trigger_name, sysname, memory_optimized_trigger>]
	ON [<schema_name, , dbo>].[<table_name, sysname, memory_optimized_table>]
	WITH NATIVE_COMPILATION, SCHEMABINDING
	AFTER <data_modification_statements, , INSERT>
AS BEGIN ATOMIC WITH
(
 TRANSACTION ISOLATION LEVEL = <transaction_isolation_level, , SNAPSHOT>, LANGUAGE = <language, , N'us_english'>
)
   --Insert statements for the trigger here
   <t-sql_statement, , declare @v int; select @v = count(*) from inserted>
END
GO
