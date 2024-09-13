--======================================================
-- Add Hash Index to a Memory Optimized Table Template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template adds a hash index to a memory optimized table.
--======================================================
USE [<database_name, sysname, memory_optimized_database>]
GO

ALTER TABLE [<schema_type, , dbo>].[<table_name, sysname, memory_optimized_table>]
	ADD INDEX <index_name, sysname, index_name> HASH (<column_name, sysname, column_name>) WITH (BUCKET_COUNT = <bucket_count, int, 131072>)
GO