--======================================================
-- Add Column to a Memory Optimized Table Template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template adds a column to a memory optimized table.
--======================================================
USE [<database_name, sysname, memory_optimized_database>]
GO

ALTER TABLE [<schema_type, , dbo>].[<table_name, sysname, memory_optimized_table>]
	ADD <new_column_name, sysname, new_column> <new_column_datatype, , int> <new_column_nullability, , NULL>
GO