--======================================================
-- Modify Column on a Memory Optimized Table Template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template modifies a column on a memory optimized table.
--======================================================
USE [<database_name, sysname, memory_optimized_database>]
GO

ALTER TABLE [<schema_type, , dbo>].[<table_name, sysname, memory_optimized_table>]
	ALTER COLUMN <column_name, sysname, column_to_modify> <column_datatype, , int> <new_column_nullability, , NULL>
GO