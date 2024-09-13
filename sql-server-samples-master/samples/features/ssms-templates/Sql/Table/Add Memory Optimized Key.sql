--======================================================
-- Add Primary Key to a Memory Optimized Table Template
-- Use the Specify Values for Template Parameters command (Ctrl-Shift-M) to fill in the parameter values below.
-- This template adds a primary key to a memory optimized table.
--======================================================
USE [<database_name, sysname, memory_optimized_database>]
GO

ALTER TABLE [<schema_type, , dbo>].[<table_name, sysname, memory_optimized_table>]
	ADD CONSTRAINT <key_name, sysname, default_key_name> PRIMARY KEY <index_type, , NONCLUSTERED> (<column_list, sysname, column_name>)
GO